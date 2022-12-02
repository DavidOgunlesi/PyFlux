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
    Height = (texture(heightMap, texCoord).y) * 64.0 - 16.0;
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
    p += normal;// * Height;
    p += vec4(0, Height, 0, 0);
    FragPos = vec3(transpose(model) * p);
    Normal = vec3(normal);
    FragPosLightSpace = lightSpaceMatrix * vec4(FragPos, 1.0);
    // ----------------------------------------------------------------------
    // output patch point position
    gl_Position = p;
    
}