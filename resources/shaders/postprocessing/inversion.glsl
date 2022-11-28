#version 330 core
  
in vec2 TexCoords;

uniform sampler2D tex;

void main()
{
    gl_FragColor = vec4(vec3(1.0 - texture(tex, TexCoords)), 1.0);
} 