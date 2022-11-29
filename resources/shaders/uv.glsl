#version 440

in vec3 FragPos;
in vec3 ourColor;
in vec2 TexCoord;
in vec3 Normal;

uniform sampler2D ourTexture;
uniform vec3 lightColor;
uniform vec3 lightPos;
uniform vec3 cameraPos;
uniform vec3 ambientColor;

out vec4 myOutputColor;
void main()
{
    // show uvs
    myOutputColor = vec4(TexCoord, 0.5, 1.0);
} 