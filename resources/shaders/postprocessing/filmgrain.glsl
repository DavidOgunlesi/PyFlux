#version 330 core
  
in vec2 TexCoords;

uniform sampler2D tex;
uniform float time;
uniform float intensity;

float random(vec2 p);

void main()
{
    gl_FragColor = texture(tex, TexCoords) * max(random(TexCoords + time), 1- intensity);
}  


float random(vec2 p)
{
    vec2 K1 = vec2(
        23.14069263277926, // e^pi (Gelfond's constant)
        2.665144142690225 // 2^sqrt(2) (Gelfond–Schneider constant)
    );
    return fract( cos( dot(p,K1) ) * 12345.6789 );
}