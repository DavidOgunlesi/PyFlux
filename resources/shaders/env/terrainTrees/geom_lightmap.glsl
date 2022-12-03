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

in float Random[];
out float Random_;

out vec4 ColorVariation_;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float gametime;
uniform vec3 cameraPos;
uniform float terrainscale;
uniform mat4 lightSpaceMatrix;
layout (binding = 8) uniform sampler2D slopeMap;

const float TREESCALE = 2;
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

mat4 rotate(float angle, vec3 v)
{
    v = normalize(v);
    float s = sin(angle);
    float c = cos(angle);
    float oc = 1.0 - c;
    
    return mat4(oc * v.x * v.x + c, oc * v.x * v.y - v.z * s, oc * v.z * v.x + v.y * s, 0.0,
                oc * v.x * v.y + v.z * s, oc * v.y * v.y + c, oc * v.y * v.z - v.x * s, 0.0,
                oc * v.z * v.x - v.y * s, oc * v.y * v.z + v.x * s, oc * v.z * v.z + c, 0.0,
                0.0, 0.0, 0.0, 1.0);
}

vec4 LookAt(vec3 point, vec4 pos){
        vec3 dir = normalize(point - ((model) * (gl_in[0].gl_Position + pos)).xyz);
        vec3 up = -sign(dir.z) * vec3(0,1,0);
        vec3 right = sign(dir.z) * vec3(1,0,0);
        vec3 rotation = vec3(dot(up, dir)*90,dot(right, dir)*90,0);
        mat4 rotMat = mat4(1.0);
        rotMat = rotate(radians(-   rotation.y), vec3(0,1,0));
        return rotMat * pos;
}

void GenerateTreeQuad(){
    //Find centre of patch
    vec4 centre = vec4(0.0);
    for (int i = 0; i<gl_in.length(); i++)
    {
        centre += (model) * gl_in[i].gl_Position;
    }
    centre /= gl_in.length();
    
    float randomNum = random(centre.xy);
    float type = int(randomNum*6);
    vec2 coord = ((centre).xz-vec2(terrainscale/2,terrainscale/2))/terrainscale;
    
    

    vec2[6] treeTexCoords = vec2[6](vec2(0.0, 0.0), vec2(0, 1.0), vec2(1.0, 1.0),vec2(0.0, 0.0), vec2(1.0, 1.0), vec2(1.0, 0.0));
    vec2[6] treeVerts = vec2[6](vec2(-1, 0.0), vec2(-1, 2), vec2(1.0, 2),vec2(-1, 0.0), vec2(1.0, 2), vec2(1.0, 0.0));
    vec4 offset = vec4(randomNum, 0 ,randomNum, 0);
    for (int i = 0; i < treeVerts.length(); i++)
    {
        TexCoord_ = treeTexCoords[i];
        FragPos_ = FragPos[i % 3];
        Normal_ = Normal[i % 3];
        FragPosLightSpace_ = FragPosLightSpace[i % 3];
        Perlin_ = Perlin[i % 3];
        Rotation_ = Rotation[i % 3];
        Height_ = Height[i % 3];
        Random_ = Random[i % 3];
        if (!(int(centre.x) % 10 == 0 && int(centre.z) % 10 == 0)){
            //gl_Position = projection * view * (model) *(gl_in[i % 3].gl_Position);
            EmitVertex();
            //gl_Position = projection * view * (model) *(gl_in[i % 3].gl_Position);
            EmitVertex();
            //gl_Position = projection * view * (model) *(gl_in[i % 3].gl_Position);
            EmitVertex();
            EndPrimitive();
            return;
        }
        float h = Height[i % 3];
        h = (h+ 16.0) / 64.0;
        float range = snoise(coord)/100;
        if (h > 0.23+range || h < 0.13+range)
         {
             break;
        }
       
        vec2 slope = (texture(slopeMap, coord+snoise(coord)/6).xy/2);
        //if slope is too steep, don't render
        float slopeVal = length(slope);
        if (slopeVal < 0.5+snoise(coord)/4){
            break;
        }

        //Ofset the vertex by the centre
        //gl_Position = vec4(treeVerts[i], 0, 0);//lerp(gl_in[i].gl_Position, centre, lerpFloat(0.5,0.7,randomNum)) + offset;

        // offset by 1 if we are middle vertex
        // if ((i+1)%gl_in.length() == 0){
        //     gl_Position = (gl_Position+ vec4(0, (randomNum+1)/1.5, 0, 0) * MAGNITUDE);
        //     // offset by noise depending on height
        //     float off = snoise(((model) * gl_Position).xz + gametime+seed);
        //     off = off/10;
        //     gl_Position = gl_Position + vec4(off, 0, off, 0);
        // }else{
        //     gl_Position = gl_Position;
        // } [col][row]
        vec4 lp = (vec4(treeVerts[i], 0, 0)*TREESCALE);
        vec4 pos = LookAt(cameraPos, lp);
        gl_Position = lightSpaceMatrix * (model) * (gl_in[0].gl_Position +vec4(pos.xyz, lp.w));
        // Add color variation 
        ColorVariation_ = vec4(random((coord+snoise(coord)))/3, random((coord+snoise(coord)))/3, 0, 1.0);

        EmitVertex();

        if ((i+1) % 3 == 0){
            EndPrimitive();
        }
    }
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
    int density = 1;
    for (int i = 0; i<density; i++) 
    {
        GenerateTreeQuad();
    }
    
}

