#version 330 core
  
in vec2 TexCoords;

uniform sampler2D tex;
uniform float power;
void main()
{
    vec2 uv = TexCoords.xy;
   
    uv *=  1.0 - uv.yx;   //vec2(1.0)- uv.yx; -> 1.-u.yx; Thanks FabriceNeyret !
    
    float vig = uv.x*uv.y * 15.0; // multiply with sth for intensity
    
    vig = pow(vig, power); // change pow for modifying the extend of the  vignette

    
    gl_FragColor = texture(tex, TexCoords)* vec4(vig); 
} 