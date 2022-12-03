#version 420
layout(triangles) in;
layout(triangle_strip, max_vertices = 6) out; //3 - terrain 3 - grass, 6 - tree

in vec3 FragPos[];
out vec3 FragPos_;

in vec3 ourColor[];
out vec3 ourColor_;

in vec2 TexCoord[];
out vec2 TexCoord_;

in vec3 Normal[];
out vec3 Normal_;

in vec4 FragPosLightSpace[];
out vec4 FragPosLightSpace_;

in float Perlin[];
out float Perlin_;

in float Rotation[];
out float Rotation_;

in float Height[];
out float Height_;

out float isGrass_;
out vec4 ColorVariation_;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float gametime;

uniform float terrainscale;
uniform mat4 lightSpaceMatrix;
layout (binding = 8) uniform sampler2D slopeMap;

const float MAGNITUDE = 0.6;
#define PI 3.1415926535897932384626433832795
vec4 lerp (vec4 a, vec4 b, float t)
{
    return a + t * (b - a);
}

float lerpFloat (float a, float b, float t)
{
    return a + t * (b - a);
}

float random (in vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}

vec3 GetNormal()
{
   vec3 a = vec3(gl_in[0].gl_Position) - vec3(gl_in[1].gl_Position);
   vec3 b = vec3(gl_in[2].gl_Position) - vec3(gl_in[1].gl_Position);
   return normalize(cross(a, b));
}  

// Simplex 2D noise
//
vec3 permute(vec3 x) { return mod(((x*34.0)+1.0)*x, 289.0); }

float snoise(vec2 v){
  const vec4 C = vec4(0.211324865405187, 0.366025403784439,
           -0.577350269189626, 0.024390243902439);
  vec2 i  = floor(v + dot(v, C.yy) );
  vec2 x0 = v -   i + dot(i, C.xx);
  vec2 i1;
  i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod(i, 289.0);
  vec3 p = permute( permute( i.y + vec3(0.0, i1.y, 1.0 ))
  + i.x + vec3(0.0, i1.x, 1.0 ));
  vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy),
    dot(x12.zw,x12.zw)), 0.0);
  m = m*m ;
  m = m*m ;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m *= 1.79284291400159 - 0.85373472095314 * ( a0*a0 + h*h );
  vec3 g;
  g.x  = a0.x  * x0.x  + h.x  * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}

void CreateGrass(float seed){
    //Find centre of patch
    vec4 centre = vec4(0.0);
    for (int i = 0; i<gl_in.length(); i++)
    {
        centre += gl_in[i].gl_Position;
    }
    centre /= gl_in.length();

    float randomNum = random(centre.xy+seed);

    vec2[3] grassTexCoords = vec2[3](vec2(0.0, 0.0), vec2(1.0, 1.0), vec2(0.0, 0.0));

    vec4 offset = vec4(randomNum, 0 ,randomNum, 0);
    for (int i = 0; i < gl_in.length(); i++)
    {
        TexCoord_ = grassTexCoords[i];
        FragPos_ = FragPos[i];
        Normal_ = Normal[i];
        FragPosLightSpace_ = FragPosLightSpace[i];
        Perlin_ = Perlin[i];
        Rotation_ = Rotation[i];
        Height_ = Height[i];
        isGrass_ = 1;
        vec2 coord = (((model) * gl_in[0].gl_Position).xz-vec2(terrainscale/2,terrainscale/2))/terrainscale;
        float h = Height[i];
        h = (h+ 16.0) / 64.0;
        float range = snoise(coord)/100;
        if (h > 0.26+range || h < 0.12+range)
         {
             break;
        }
       
        vec2 slope = (texture(slopeMap, coord+snoise(coord+seed)/6).xy/2);
        //if slope is too steep, don't render
        float slopeVal = length(slope);
        if (slopeVal < 0.5+snoise(coord)/4){
            break;
        }

        //Ofset the vertex by the centre
        gl_Position = lerp(gl_in[i].gl_Position, centre, lerpFloat(0.5,0.7,randomNum)) + offset;

        // offset by 1 if we are middle vertex
        if ((i+1)%gl_in.length() == 0){
            gl_Position = (gl_Position+ vec4(0, (randomNum+1)/1.5, 0, 0) * MAGNITUDE);
            // offset by noise depending on height
            float off = snoise(((model) * gl_Position).xz + gametime+seed);
            off = off/10;
            gl_Position = gl_Position + vec4(off, 0, off, 0);
        }else{
            gl_Position = gl_Position;
        }

        gl_Position = lightSpaceMatrix * (model) * gl_Position;
        
        // Add color variation 
        ColorVariation_ = vec4(random((coord+snoise(coord+seed)))/3, random((coord+snoise(coord+seed)))/3, 0, 1.0);

        EmitVertex();
    }
    EndPrimitive();
}

void Cylinder(){
    int verticesCyl = 60;
    int indicesCyl = verticesCyl + 2;
    float cylHeight = .2;
    float theta = 0.0;
    for (int j = 0; j < verticesCyl*3 ; j+=3) {
        float x = cos(theta);
        float y = sin(theta);
        float z = j % 2 == 0 ? cylHeight : -cylHeight;
        vec3 pos = vec3(j, j, j);
        gl_Position = (gl_in[0].gl_Position + vec4(pos, 1.0));
        EmitVertex();
        theta += 2 * PI / (verticesCyl);
    }
    gl_Position = projection * view * (model) * gl_Position;
    EndPrimitive();
}

void branch(float size, int depth){

}

void trunk(float size, int depth){
    branch(size*0.9, depth);
}



void main()
{
    isGrass_ = 0;
    for (int i = 0; i<gl_in.length(); i++)
    {
        TexCoord_ = TexCoord[i];
        FragPos_ = FragPos[i];
        Normal_ = Normal[i];
        FragPosLightSpace_ = FragPosLightSpace[i];
        Perlin_ = Perlin[i];
        Rotation_ = Rotation[i];
        Height_ = Height[i];
        gl_Position = projection * view * (model) * gl_in[i].gl_Position;
        EmitVertex();
    }

    EndPrimitive();
    int density = 1;
    for (int i = 0; i<density; i++) 
    {
        CreateGrass(1000*i);
    }
    
}

