#version 330 core
  
in vec2 TexCoords;

uniform sampler2D tex;

void main()
{
    gl_FragColor = texture(tex, TexCoords);
    float average = 0.2126 *  gl_FragColor.r + 0.7152 *  gl_FragColor.g + 0.0722 *  gl_FragColor.b;
    gl_FragColor = vec4(average, average, average, 1.0);
}  