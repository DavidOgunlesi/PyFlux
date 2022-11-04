#version 330
vec4 FragColor;
in vec3 ourColor;
in vec2 TexCoord;

uniform sampler2D ourTexture;

void main()
{
    gl_FragColor = texture(ourTexture, TexCoord) * vec4(ourColor, 1.0);
} 