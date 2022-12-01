#version 440 core

layout (quads, equal_spacing, ccw) in;

in vec3 FragPos_[];
in vec3 ourColor_[];
in vec2 TexCoord_[];
in vec3 Normal_[];
in vec4 FragPosLightSpace_[];
in mat4 model_[];
in float Perlin_[];
in float Rotation_[];
out vec3 FragPos;
out vec3 ourColor;
out vec2 TexCoord;
out vec3 Normal;
out vec4 FragPosLightSpace;
out float Rotation;
// send to Fragment Shader for coloring
out float Height;
out float Perlin;

layout (binding = 3) uniform sampler2D heightMap;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 lightSpaceMatrix;
uniform float time;

struct Wave {
    float Wavelength;
    float Steepness;
    vec2 Direction;
};

vec3 GerstnerWave (Wave wave, vec3 p, inout vec3 tangent, inout vec3 binormal);
float snoise(vec2 v);
vec3 permute(vec3 x);
float random (in vec2 st);
float noise (in vec2 st);
float fbm (in vec2 st);

void main(){
    // get patch coordinate
    float u = gl_TessCoord.x;
    float v = gl_TessCoord.y;

    // ----------------------------------------------------------------------
    // retrieve control point texture coordinates
    vec2 t00 = TexCoord_[0];
    vec2 t01 = TexCoord_[1];
    vec2 t10 = TexCoord_[2];
    vec2 t11 = TexCoord_[3];

    // bilinearly interpolate texture coordinate across patch
    vec2 t0 = (t01 - t00) * u + t00;
    vec2 t1 = (t11 - t10) * u + t10;
    vec2 texCoord = (t1 - t0) * v + t0;

    TexCoord = texCoord;
    
    // bilinearly interpolate perlin noises across patch
    // retrieve control point texture coordinates
    float pn00 = Perlin_[0];
    float pn01 = Perlin_[1];
    float pn10 = Perlin_[2];
    float pn11 = Perlin_[3];
    float pn0 = (pn01 - pn00) * u + pn00;
    float pn1 = (pn11 - pn10) * u + pn10;
    float finalPerlin = (pn1 - pn0) * v + pn0;
    Perlin = finalPerlin;
    // bilinearly interpolate rotation noises across patch
    // retrieve control point texture coordinates
    Rotation = Rotation_[0];

    // lookup texel at patch coordinate for height and scale + shift as desired
    Height = (texture(heightMap, texCoord).y/2) * 64.0 - 16.0;
    // Ramp values below a certain height down
    if (Height < 10.0) {
        Height = Height * 1.5;
    }
    // ----------------------------------------------------------------------
    // retrieve control point position coordinates
    vec4 p00 = gl_in[0].gl_Position;
    vec4 p01 = gl_in[1].gl_Position;
    vec4 p10 = gl_in[2].gl_Position;
    vec4 p11 = gl_in[3].gl_Position;

    // compute patch surface normal
    vec4 uVec = p01 - p00;
    vec4 vVec = p10 - p00;
    vec4 normal = normalize( vec4(cross(vVec.xyz, uVec.xyz), 0) );

    // bilinearly interpolate position coordinate across patch
    vec4 p0 = (p01 - p00) * u + p00;
    vec4 p1 = (p11 - p10) * u + p10;
    vec4 p = (p1 - p0) * v + p0;

    // displace point along normal
    p += normal * Height;
    
    Perlin = snoise(p.xz/30+time);
    float Perlin2 = snoise(p.xz*30+time);
    //Waves using gerstner waves
    //float _Wavelength = 10;
    //float _Steepness = 0.5;
    //vec2 _Direction = vec2(1.0, 1.0);
    float fbm_ = (fbm(p.xz/15+time/100));
    Wave _WaveA = Wave(7/3, 0.5/2, vec2(fbm_/3, 1-fbm_/3));
    Wave _WaveB = Wave(5/3, 0.25/2, vec2(1-fbm_, fbm_));
    Wave _WaveC = Wave(1, 0.15/2, vec2(1, 1)); 
    Wave _WaveD = Wave(.1, 0.1, vec2(1, 1)); 
    vec3 tangent = vec3(1, 0, 0);
    vec3 binormal = vec3(0, 0, 1);
    //p += GerstnerWave(_WaveA, p.xyz, tangent, binormal);
    vec3 point = p.xyz;
    vec3 newp = point;
    newp += GerstnerWave(_WaveA, point, tangent, binormal);
    newp += GerstnerWave(_WaveB, point, tangent, binormal);
    newp += GerstnerWave(_WaveC, point, tangent, binormal);
    newp += GerstnerWave(_WaveD, point, tangent, binormal);
    p.xyz = newp;
    
    Normal = normalize(cross(binormal, tangent));
    p.y += Perlin/2/4;
    p.y += Perlin2/10/4;
    p.y+= fbm(p.xz/5+time)/10/4;
    FragPos = vec3(model * p);
    FragPosLightSpace = lightSpaceMatrix * vec4(FragPos, 1.0);
    // ----------------------------------------------------------------------
    // output patch point position in clip space
    gl_Position = lightSpaceMatrix * transpose(model) * p;
    
}

vec3 GerstnerWave (Wave wave, vec3 p, inout vec3 tangent, inout vec3 binormal) {
        float _Time = time;
    float PI = 3.14159265359;
    float steepness = wave.Steepness;
    float wavelength = wave.Wavelength;
    float k = 2 * PI / wavelength;
    float c = sqrt(9.8 / k);
    vec2 d = normalize(wave.Direction);
    float f = k * (dot(d, p.xz) - c * _Time);
    float a = steepness / k;

    tangent += vec3(
        -d.x * d.x * (steepness * sin(f)),
        d.x * (steepness * cos(f)),
        -d.x * d.y * (steepness * sin(f))
    );
    binormal += vec3(
        -d.x * d.y * (steepness * sin(f)),
        d.y * (steepness * cos(f)),
        -d.y * d.y * (steepness * sin(f))
    );
    p = vec3(
        d.x * (a * cos(f)),
        a * sin(f),
        d.y * (a * cos(f))
    );
    return p;
}

// Simplex 2D noise
//
vec3 permute(vec3 x) { return mod(((x*34.0)+1.0)*x, 289.0); }

float snoise(vec2 v){
  const vec4 C = vec4(0.211324865405187, 0.366025403784439,
           -0.577350269189626, 0.024390243902439);
  vec2 i  = floor(v + dot(v, C.yy) );
  vec2 x0 = v -   i + dot(i, C.xx);
  vec2 i1;
  i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod(i, 289.0);
  vec3 p = permute( permute( i.y + vec3(0.0, i1.y, 1.0 ))
  + i.x + vec3(0.0, i1.x, 1.0 ));
  vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy),
    dot(x12.zw,x12.zw)), 0.0);
  m = m*m ;
  m = m*m ;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m *= 1.79284291400159 - 0.85373472095314 * ( a0*a0 + h*h );
  vec3 g;
  g.x  = a0.x  * x0.x  + h.x  * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}

// Author @patriciogv - 2015
// http://patriciogonzalezvivo.com

#ifdef GL_ES
precision mediump float;
#endif

float random (in vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}

// Based on Morgan McGuire @morgan3d
// https://www.shadertoy.com/view/4dS3Wd
float noise (in vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);

    // Four corners in 2D of a tile
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(a, b, u.x) +
            (c - a)* u.y * (1.0 - u.x) +
            (d - b) * u.x * u.y;
}

#define OCTAVES 6
float fbm (in vec2 st) {
    // Initial values
    float value = 0.0;
    float amplitude = .5;
    float frequency = 0.;
    //
    // Loop of octaves
    for (int i = 0; i < OCTAVES; i++) {
        value += amplitude * noise(st);
        st *= 2.;
        amplitude *= .5;
    }
    return value;
}
