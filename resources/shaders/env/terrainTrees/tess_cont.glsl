#version 440 core

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

in float Random[];
out float Random_[];

in float Perlin[];
out float Perlin_[];
in float Rotation[];
out float Rotation_[];
uniform mat4 model;
uniform mat4 view;

// ----------------------------------------------------------------------
// Step 1: define constants to control tessellation parameters
uniform int MIN_TESS_LEVEL;// = 1;
uniform int MAX_TESS_LEVEL;// = 64;
uniform float MIN_DISTANCE;// = 0;
uniform float MAX_DISTANCE;// = 80;


void main()
{
    // ----------------------------------------------------------------------
    // pass attributes through
    gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
    TexCoord_[gl_InvocationID] = TexCoord[gl_InvocationID];
    FragPos_[gl_InvocationID] = FragPos[gl_InvocationID];
    Normal_[gl_InvocationID] = Normal[gl_InvocationID];
    FragPosLightSpace_[gl_InvocationID] = FragPosLightSpace[gl_InvocationID];
    Perlin_[gl_InvocationID] = Perlin[gl_InvocationID];
    Rotation_[gl_InvocationID] = Rotation[gl_InvocationID];
    Random_[gl_InvocationID] = Random[gl_InvocationID];
    // ----------------------------------------------------------------------
    // invocation zero controls tessellation levels for the entire patch
    if (gl_InvocationID == 0)
    {
        // ----------------------------------------------------------------------
        // Step 2: transform each vertex into eye space
        vec4 eyeSpacePos00 = view * model * gl_in[0].gl_Position;
        vec4 eyeSpacePos01 = view * model * gl_in[1].gl_Position;
        vec4 eyeSpacePos10 = view * model * gl_in[2].gl_Position;
        vec4 eyeSpacePos11 = view * model * gl_in[3].gl_Position;

        // ----------------------------------------------------------------------
        // Step 3: "distance" from camera scaled between 0 and 1
        float distance00 = clamp((abs(eyeSpacePos00.z)-MIN_DISTANCE) / (MAX_DISTANCE-MIN_DISTANCE), 0.0, 1.0);
        float distance01 = clamp((abs(eyeSpacePos01.z)-MIN_DISTANCE) / (MAX_DISTANCE-MIN_DISTANCE), 0.0, 1.0);
        float distance10 = clamp((abs(eyeSpacePos10.z)-MIN_DISTANCE) / (MAX_DISTANCE-MIN_DISTANCE), 0.0, 1.0);
        float distance11 = clamp((abs(eyeSpacePos11.z)-MIN_DISTANCE) / (MAX_DISTANCE-MIN_DISTANCE), 0.0, 1.0);

        // ----------------------------------------------------------------------
        // Step 4: interpolate edge tessellation level based on closer vertex
        float tessLevel0 = mix( MAX_TESS_LEVEL, MIN_TESS_LEVEL, min(distance10, distance00) );
        float tessLevel1 = mix( MAX_TESS_LEVEL, MIN_TESS_LEVEL, min(distance00, distance01) );
        float tessLevel2 = mix( MAX_TESS_LEVEL, MIN_TESS_LEVEL, min(distance01, distance11) );
        float tessLevel3 = mix( MAX_TESS_LEVEL, MIN_TESS_LEVEL, min(distance11, distance10) );

        // ----------------------------------------------------------------------
        // Step 5: set the corresponding outer edge tessellation levels
        gl_TessLevelOuter[0] = tessLevel0;
        gl_TessLevelOuter[1] = tessLevel1;
        gl_TessLevelOuter[2] = tessLevel2;
        gl_TessLevelOuter[3] = tessLevel3;

        // ----------------------------------------------------------------------
        // Step 6: set the inner tessellation levels to the max of the two parallel edges
        gl_TessLevelInner[0] = max(tessLevel1, tessLevel3);
        gl_TessLevelInner[1] = max(tessLevel0, tessLevel2);
    }
}

