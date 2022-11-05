#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;
layout (location = 3) in vec3 aNorm;

out vec3 FragPos;
out vec3 ourColor;
out vec2 TexCoord;
out vec3 Normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    FragPos =  vec3(projection * view * model * vec4(aPos, 1.0));
    ourColor = aColor;
    TexCoord = aTexCoord;
    //to do generate on CPU
    mat3 NormalMat = mat3(transpose(inverse(model)));
    Normal = NormalMat * aNorm;
}