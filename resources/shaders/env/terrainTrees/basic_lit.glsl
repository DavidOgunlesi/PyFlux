#version 440 core

in vec3 FragPos_;
in vec3 ourColor_;
in vec2 TexCoord_;
in vec3 Normal_;
in vec4 FragPosLightSpace_;

in float Height_;
in float Rotation_;
in float Perlin_;
in vec4 ColorVariation_;
in float Random_;
uniform vec3 cameraPos;

struct DirLight {
    vec3 direction;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

struct PointLight {
    bool set;
    vec3 position;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    
    float constant;
    float linear;
    float quadratic;
};



struct SpotLight {
    bool set;
    vec3 position;
    vec3 direction;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float cutOff;
    float outerCutOff;

    float constant;
    float linear;
    float quadratic;
};

struct Material {
    sampler2D diffuse;
    sampler2D specular;
    float roughness;
}; 

uniform Material material;

uniform DirLight dirLight; 

#define NR_POINT_LIGHTS 4  
uniform PointLight pointLights[NR_POINT_LIGHTS];
#define NR_SPOT_LIGHTS 4  
uniform SpotLight spotLights[NR_SPOT_LIGHTS];   

uniform samplerCube skybox;
uniform sampler2D shadowMap;
uniform int terrainTiling;

layout (binding = 20) uniform sampler2D tree0;
layout (binding = 21) uniform sampler2D tree1;
layout (binding = 22) uniform sampler2D tree2;
layout (binding = 23) uniform sampler2D tree3;
layout (binding = 24) uniform sampler2D tree4;
layout (binding = 25) uniform sampler2D tree5;
layout (binding = 26) uniform sampler2D tree6;

float ShadowCalculation(DirLight light, vec3 normal, vec4 fragPosLightSpace);
float CalculateSpecComponent(vec3 lightDir, vec3 normal, vec3 viewDir);
vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir, float shadow, vec4 diffuseCol);  
vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir, float shadow, vec4 diffuseCol);  
vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir, float shadow, vec4 diffuseCol);  
vec4 GetTerrainColor(vec3 norm, vec3 viewDir, float shadow);

vec4 LinearGradient(float value, vec4[6] colors, float[6] locations) {
    if (value <= locations[0]) {
        return colors[0];
    }
    if (value >= locations[locations.length() - 1]) {
        return colors[colors.length() - 1];
    }
    for (int i = 0; i < locations.length() - 1; i++) {
        if (value >= locations[i] && value <= locations[i + 1]) {
            float t = (value - locations[i]) / (locations[i + 1] - locations[i]) + Perlin_/10;
            return mix(colors[i], colors[i + 1], t);
        }
    }
    return vec4(0.0, 0.0, 0.0, 1.0);
}

float random(vec2 p)
{
    vec2 K1 = vec2(
        23.14069263277926, // e^pi (Gelfond's constant)
        2.665144142690225 // 2^sqrt(2) (Gelfond–Schneider constant)
    );
    return fract( cos( dot(p,K1) ) * 12345.6789 );
}


void main()
{
    vec3 norm = normalize(Normal_);
    vec3 viewDir = normalize(cameraPos - FragPos_);
    //Shadow
    float shadow = ShadowCalculation(dirLight, norm, FragPosLightSpace_); 
    vec4 texColor = vec4(1.0, 1.0, 1.0, 1.0);
    float num = clamp(Random_*Perlin_*6, 0, 6);
    if (int(num) == 0){
        texColor = texture(tree0, -TexCoord_);
    }
    else if (int(num)== 1){
        texColor = texture(tree1, -TexCoord_);
    }
    else if (int(num) == 2){
        texColor = texture(tree2, -TexCoord_);
    }
    else if (int(num) == 3){
        texColor = texture(tree3, -TexCoord_);
    }
    else if (int(num) == 4){
        texColor = texture(tree4, -TexCoord_);
    }
    else if (int(num) == 5){
        texColor = texture(tree5, -TexCoord_);
    }
    else if (int(num) == 6){
        texColor = texture(tree6, -TexCoord_);
    }
    if (texColor.a <= 0.5) {
        discard;
    }

    //int(6*random(treePos_.xz))
    vec4 grassColor = texColor * ColorVariation_;
    // phase 1: Directional lighting
    vec3 finalGrassColor = CalcDirLight(dirLight, norm, viewDir, shadow, grassColor);
    // phase 2: Point lights
    for(int i = 0; i < NR_POINT_LIGHTS; i++){   
        if (pointLights[i].set == false){
            continue;
        }else{
            finalGrassColor += CalcPointLight(pointLights[i], norm, FragPos_, viewDir, shadow, grassColor);    
        } 
    }   
    // phase 3: Spot lights
    for(int i = 0; i < NR_SPOT_LIGHTS; i++){
        if (spotLights[i].set == false){
            continue;
        }else{
            finalGrassColor += CalcSpotLight(spotLights[i], norm, FragPos_, viewDir, shadow, grassColor);
        }
    }

    gl_FragColor = vec4(finalGrassColor,1);//vec4(mix(finalTerrainColor, finalGrassColor, isGrass_),1);
    
} 


float ShadowCalculation(DirLight light, vec3 normal, vec4 fragPosLightSpace){
    // perform perspective divide
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    // transform to [0,1] range
    projCoords = projCoords * 0.5 + 0.5;
    // get closest depth value from light's perspective (using [0,1] range fragPosLight as coords)
    float closestDepth = texture(shadowMap, projCoords.xy).r; 
    // get depth of current fragment from light's perspective
    float currentDepth = projCoords.z;
    // check whether current frag pos is in shadow 
    //with bias to stop shadow acne
    vec3 lightDir = normalize(light.direction);
    float bias = max(0.010 * (1.0 - dot(normal, lightDir)), 0.005);  
    //float shadow = currentDepth - bias > closestDepth  ? 1.0 : 0.0; 

    //PCF - percentage-closer filtering
    float shadow = 0.0;
    vec2 texelSize = 1.0 / textureSize(shadowMap, 0);
    int numberOfSamples = 9;
    for(int x = -numberOfSamples/9; x <= numberOfSamples/9; ++x)
    {
        for(int y = -numberOfSamples/9; y <= numberOfSamples/9; ++y)
        {
            float pcfDepth = texture(shadowMap, projCoords.xy + vec2(x, y) * texelSize).r; 
            shadow += currentDepth - bias > pcfDepth ? 1.0 : 0.0;        
        }    
    }
    shadow /= numberOfSamples;
    // Stop shadow appearing when areas are outside of the light frustum
    if(projCoords.z > 1.0)
        shadow = 0.0;

    return shadow;
}

//Blinn Phong specular
float CalculateSpecComponent(vec3 lightDir, vec3 normal, vec3 viewDir){
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), material.roughness);
   //vec3 reflectDir = reflect(-lightDir, normal);  
   //float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
   return spec;
}

vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir, float shadow, vec4 diffuseCol){
    // diffuse 
    vec3 lightDir = normalize(light.direction);
    float diff = max(dot(normal, lightDir), 0.0);
    
    // specular
    //vec3 reflectDir = reflect(-lightDir, normal);  
    //float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    float spec = CalculateSpecComponent(lightDir, normal, viewDir);

    // Combine
    vec3 ambient  = light.ambient * vec3(diffuseCol);
    vec3 diffuse  = light.diffuse * diff * vec3(diffuseCol); 
    //vec3 specular = light.specular * spec * vec3(texture(material.specular, TexCoord_)); 

    return (ambient + (1.0 - shadow) * (diffuse));
}

vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir, float shadow, vec4 diffuseCol){
    vec3 lightDir = normalize(light.position - fragPos);

    // diffuse 
    float diff = max(dot(normal, lightDir), 0.0);
    // specular
    //vec3 reflectDir = reflect(-lightDir, normal);  
    //float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    float spec = CalculateSpecComponent(lightDir, normal, viewDir);
    // light attenuation
    float dist    = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * dist + light.quadratic * (dist * dist));

    vec3 ambient = light.ambient * vec3(diffuseCol);
    vec3 diffuse = light.diffuse * diff * vec3(diffuseCol); 
    //vec3 specular = light.specular * (spec *  vec3(texture(material.specular, TexCoord_)));  
    
    ambient  *= attenuation; 
    diffuse  *= attenuation;
    //specular *= attenuation; 

    return  (ambient + (1.0 - shadow) * (diffuse));
}

vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir, float shadow, vec4 diffuseCol){
    
    // diffuse 
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);

    // specular
    //vec3 reflectDir = reflect(-lightDir, normal);  
    //float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    float spec = CalculateSpecComponent(lightDir, normal, viewDir);
    // light attenuation
    float distance    = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));  
    
    //use ambient light so scene isn't completely dark outside the spotlight.
    float theta     = dot(lightDir, normalize(-light.direction));
    float epsilon   = light.cutOff - light.outerCutOff;
    float intensity = clamp((theta - light.outerCutOff) / epsilon, 0.0, 1.0); 
    
    vec3 ambient = light.ambient * vec3(diffuseCol);
    vec3 diffuse = light.diffuse * diff * vec3(diffuseCol); 
    //vec3 specular = light.specular * (spec *  vec3(texture(material.specular, TexCoord_))); 

    ambient  *= attenuation; 
    diffuse  *= attenuation;
    //specular *= attenuation; 

    diffuse  *= intensity;
    //specular *= intensity; 

   return  (ambient + (1.0 - shadow) * (diffuse));
}