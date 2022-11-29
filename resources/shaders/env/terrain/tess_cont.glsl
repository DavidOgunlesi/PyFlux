#version 330 core
#extension GL_ARB_tessellation_shader : enable

layout (vertices = 4) out;

in vec3 FragPos[];
out vec3 FragPos_[];
in vec3 ourColor[];
out vec3 ourColor_[];
in vec2 TexCoord[];
out vec2 TexCoord_[];
in vec3 Normal[];
out vec3 Normal_[];
in vec4 FragPosLightSpace[];
out vec4 FragPosLightSpace_[];

uniform vec3 cameraPos;
vec4 camPos = vec4(2.0 * cameraPos - 1.0, 0.0); // get in range [-1, 1]

const int MIN_TES = 2;
const int MAX_TES = 16;
const float MIN_DIST = 0.0;
const float MAX_DIST = 1.5;

void main()
{
    gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
    TexCoord_[gl_InvocationID] = TexCoord[gl_InvocationID];

    if (gl_InvocationID == 0)
    {
        vec4 center0 = gl_in[0].gl_Position + (gl_in[3].gl_Position - gl_in[0].gl_Position) / 2.0; // left side
        vec4 center1 = gl_in[1].gl_Position + (gl_in[0].gl_Position - gl_in[1].gl_Position) / 2.0; // bot side
        vec4 center2 = gl_in[2].gl_Position + (gl_in[1].gl_Position - gl_in[2].gl_Position) / 2.0; // right side
        vec4 center3 = gl_in[3].gl_Position + (gl_in[2].gl_Position - gl_in[3].gl_Position) / 2.0; // top side
        
        float dist0 = length(camPos - center0);
        float dist1 = length(camPos - center1);
        float dist2 = length(camPos - center2);
        float dist3 = length(camPos - center3);

        int tes0 = int(mix(MAX_TES, MIN_TES, clamp(dist0 / MAX_DIST, 0.0, 1.0)));
        int tes1 = int(mix(MAX_TES, MIN_TES, clamp(dist1 / MAX_DIST, 0.0, 1.0)));
        int tes2 = int(mix(MAX_TES, MIN_TES, clamp(dist2 / MAX_DIST, 0.0, 1.0)));
        int tes3 = int(mix(MAX_TES, MIN_TES, clamp(dist3 / MAX_DIST, 0.0, 1.0)));

        gl_TessLevelOuter[0] = tes0; // left for quads
        gl_TessLevelOuter[1] = tes1; // bot for quads
        gl_TessLevelOuter[2] = tes2; // right for quads
        gl_TessLevelOuter[3] = tes3; // top for quads
        
        gl_TessLevelInner[0] = max(tes1, tes3); // top bot for quads
        gl_TessLevelInner[1] = max(tes0, tes2); // left right for quads
    }
}