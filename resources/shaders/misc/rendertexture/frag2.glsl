#version 330 core
  
in vec2 TexCoords;

uniform sampler2D tex;

void main()
{ 
    gl_FragColor = vec4(1,0.5,1,1) * texture(tex, TexCoords);
    //vec4(TexCoords, 1.0, 1.0);
}