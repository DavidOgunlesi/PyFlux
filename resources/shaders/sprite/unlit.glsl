#version 330

in vec2 TexCoord;
uniform sampler2D ourTexture;
uniform vec4 SpriteColor;

void main()
{
    vec4 texColor = texture(ourTexture, TexCoord);
    if(texColor.a < 0.5)
        discard;
    texColor = SpriteColor;
    gl_FragColor = texColor;
} 