#version 330 core
  
in vec2 TexCoords;

uniform sampler2D tex;

void main()
{ 
    gl_FragColor = texture(tex, TexCoords);
}