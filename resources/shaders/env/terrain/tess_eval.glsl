#version 440 core
#extension GL_ARB_tessellation_shader : enable

layout (quads, equal_spacing, ccw) in;

in vec3 FragPos_[];
in vec3 ourColor_[];
in vec2 TexCoord_[];
in vec3 Normal_[];
in vec4 FragPosLightSpace_[];

out vec3 FragPos;
out vec3 ourColor;
out vec2 TexCoord;
out vec3 Normal;
out vec4 FragPosLightSpace;

void main(){
    float u = gl_TessCoord.x;
    float v = gl_TessCoord.y;

    vec2 uv0 = TexCoord_[0];
    vec2 uv1 = TexCoord_[1];
    vec2 uv2 = TexCoord_[2];
    vec2 uv3 = TexCoord_[3];

    vec2 leftUv = uv0 + v * (uv3 - uv0);
    vec2 rightUv = uv1 + v * (uv2 - uv1);
    vec2 uv = leftUv + u * (rightUv - leftUv);

    vec4 pos0 = gl_in[0].gl_Position;
    vec4 pos1 = gl_in[1].gl_Position;
    vec4 pos2 = gl_in[2].gl_Position;
    vec4 pos3 = gl_in[3].gl_Position;

    vec4 leftPos = pos0 + v * (pos3 - pos0);
    vec4 rightPos = pos1 + v * (pos2 - pos1);
    vec4 pos = leftPos + u * (rightPos - leftPos);

    gl_Position = pos;
    TexCoord = uv;
    
}