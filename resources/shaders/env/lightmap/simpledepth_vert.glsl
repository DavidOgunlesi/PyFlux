#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 4) in mat4 modelInstanceMatrix;

uniform mat4 lightSpaceMatrix;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = lightSpaceMatrix * transpose(modelInstanceMatrix) * vec4(aPos, 1.0);
}  