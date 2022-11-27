#version 330 core
  
in vec2 TexCoords;

uniform sampler2D shadowMap;
uniform vec3 test;


void main()
{ 
    gl_FragColor = texture(shadowMap, TexCoords);
}