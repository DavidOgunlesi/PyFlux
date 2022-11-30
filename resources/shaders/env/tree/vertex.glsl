#version 440 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;
layout (location = 3) in vec3 aNorm;
layout (location = 4) in mat4 modelInstanceMatrix;

out vec3 FragPos;
out vec3 ourColor;
out vec2 TexCoord;
out vec3 Normal;
out vec4 FragPosLightSpace;
out mat4 MVP;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 lightSpaceMatrix;
uniform float terrainscale;
layout (binding = 3) uniform sampler2D heightMap;


void main()
{
    // transpose bc numpy is column major and opengl is row major AHHH this was annoying to figure out
    mat4 modelInstMtx = transpose(modelInstanceMatrix);

    
    
    //to do generate on CPU
    mat3 NormalMat = mat3(transpose(inverse(modelInstMtx)));
    Normal = NormalMat * aNorm;

    //vec3 offset = vec3(model * vec4(aPos, 1.0));
    FragPos = vec3(model * modelInstMtx * vec4(aPos, 1.0));
    
    // lookup texel at patch coordinate for height and scale + shift as desired
    float Height = (texture(heightMap, (FragPos.xz-vec2(terrainscale/2,terrainscale/2))/terrainscale).y/2) * 64.0 - 16.0;
    
    MVP = projection * view * modelInstMtx;
     if (Height < 10.0) {
        Height = Height * 1.5;
    }

    if (Height < -10000.0 || Height < -0) {
        // draw off screen
        gl_Position =  vec4(5,5,5,5);
    }else{
        gl_Position =  projection * view * vec4(FragPos + vec3(0, Height*100, 0),1);
    }
    
    ourColor = aColor;
    TexCoord = aTexCoord;
    FragPosLightSpace = lightSpaceMatrix * vec4(FragPos, 1.0);
    
    
}