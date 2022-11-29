#version 330 core
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

uniform mat4 view;
uniform mat4 projection;
uniform mat4 lightSpaceMatrix;
uniform sampler2D heightMap;

void main()
{
    // transpose bc numpy is column major and opengl is row major AHHH this was annoying to figure out
    mat4 modelMtx = transpose(modelInstanceMatrix);
    
    vec4 pos = vec4( aPos, 1.0); //vec4(aPos.x, y, aPos.z, 1.0);
    gl_Position =  /*projection * view * modelMtx */ pos;

    FragPos = vec3(modelMtx * pos);
    ourColor = aColor;
    TexCoord = aTexCoord;
    FragPosLightSpace = lightSpaceMatrix * vec4(FragPos, 1.0);
    
    //to do generate on CPU
    mat3 NormalMat = mat3(transpose(inverse(modelMtx)));
    Normal = NormalMat * aNorm;
}