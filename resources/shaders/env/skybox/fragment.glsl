#version 440

in vec3 TexCoord;
uniform samplerCube skybox;
out vec4 myOutputColor;

void main()
{
    myOutputColor = texture(skybox, TexCoord);
} 