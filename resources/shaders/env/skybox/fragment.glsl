#version 330

in vec3 TexCoord;
uniform samplerCube skybox;

void main()
{
    gl_FragColor = texture(skybox, TexCoord);
} 