#version 440 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;
layout (location = 3) in vec3 aNorm;
layout (location = 4) in mat4 modelInstanceMatrix;

out vec3 FragPos;
out vec3 ourColor;
out vec2 TexCoord;
out vec3 Normal;
out vec4 FragPosLightSpace;
out mat4 MVP;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 lightSpaceMatrix;
uniform float terrainscale;
layout (binding = 3) uniform sampler2D heightMap;
layout (binding = 4) uniform sampler2D slopeMap;

vec3 permute(vec3 x);
float snoise(vec2 v);

void main()
{
    // transpose bc numpy is column major and opengl is row major AHHH this was annoying to figure out
    mat4 modelInstMtx = transpose(modelInstanceMatrix);

    
    
    //to do generate on CPU
    mat3 NormalMat = mat3(transpose(inverse(modelInstMtx)));
    Normal = NormalMat * aNorm;

    vec3 FragPosWithoutSlope = vec3(model * modelInstMtx * vec4(aPos, 1.0));
    // convert slope map derivative to rotation matrix
    vec2 coord = (FragPosWithoutSlope.xz-vec2(terrainscale/2,terrainscale/2))/terrainscale;
    float slope = (texture(slopeMap, coord+snoise(coord)/300).y/2);
    //if slope is too steep, don't render
    float slopeVal = length(slope);
    vec3 off = vec3(0,0,0);
    if (slopeVal < 0.5){
       off = vec3(-11000,-11000,-11000);
    }
    // mat4 slopeMat = mat4(1.0);
    // slopeMat[0][0] = slope.x;
    // slopeMat[0][1] = slope.y;
    // slopeMat[1][0] = slope.z;
    
    //vec3 offset = vec3(model * vec4(aPos, 1.0));
    FragPos = vec3(model * modelInstMtx * vec4(aPos, 1.0));
    
    // lookup texel at patch coordinate for height and scale + shift as desired
    float Height = (texture(heightMap, (FragPosWithoutSlope.xz-vec2(terrainscale/2,terrainscale/2))/terrainscale).y/2) * 64.0 - 16.0;
    
    MVP = projection * view * modelInstMtx;
     if (Height < 10.0) {
        Height = Height * 1.5;
    }

    if ((Height+16)/64 < 0.5 || (Height+16)/64 < 0.7){
       off = vec3(-11000,-11000,-11000);
    }
    
    gl_Position =  projection * view * vec4(FragPos + off + vec3(0, Height*100, 0),1);
    
    
    ourColor = aColor;
    TexCoord = aTexCoord;
    FragPosLightSpace = lightSpaceMatrix * vec4(FragPos + vec3(0, Height*100, 0),1);
    
    
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