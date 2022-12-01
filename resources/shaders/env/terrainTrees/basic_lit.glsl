#version 440 core

in vec3 FragPos_;
in vec3 ourColor_;
in vec2 TexCoord_;
in vec3 Normal_;
in vec4 FragPosLightSpace_;

in float Height_;
in float Rotation_;
in float Perlin_;
in float isGrass_;
in vec4 ColorVariation_;
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

layout (binding = 4) uniform sampler2D grassTexture;
layout (binding = 5) uniform sampler2D sandTexture;
layout (binding = 6) uniform sampler2D dirtTexture;
layout (binding = 7) uniform sampler2D waterTexture;
layout (binding = 8) uniform sampler2D slopeMap;
layout (binding = 9) uniform sampler2D grassBladeTexture;

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

    vec4 terrainColor = GetTerrainColor(norm, viewDir, shadow);


    // phase 1: Directional lighting
    vec3 finalTerrainColor = CalcDirLight(dirLight, norm, viewDir, shadow, terrainColor);
    // phase 2: Point lights
    for(int i = 0; i < NR_POINT_LIGHTS; i++){   
        if (pointLights[i].set == false){
            continue;
        }else{
            finalTerrainColor += CalcPointLight(pointLights[i], norm, FragPos_, viewDir, shadow, terrainColor);    
        } 
    }   
    // phase 3: Spot lights
    for(int i = 0; i < NR_SPOT_LIGHTS; i++){
        if (spotLights[i].set == false){
            continue;
        }else{
            finalTerrainColor += CalcSpotLight(spotLights[i], norm, FragPos_, viewDir, shadow, terrainColor);
        }
    }
    
    vec4 grassColor = texture(grassBladeTexture, TexCoord_) * ColorVariation_;
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

    
    gl_FragColor = vec4(TexCoord_, 0 , 1);//vec4(mix(finalTerrainColor, finalGrassColor, isGrass_),1);
    
} 

vec4 GetTerrainColor(vec3 norm, vec3 viewDir, float shadow){
    // Environment mapping
    vec3 envReflect = reflect(viewDir, norm);

    //Refraction
    float ratio = 1.00 / 4.52;
    vec3 envRefract = refract(viewDir, norm, ratio);

    vec3 R = envReflect;
    R *= vec3(1, -1, 1);

    float h = (Height_ + 16)/64.0f;
	vec4 heightCol = vec4(h, h, h, 1.0);
    
    const int numberOfTextures = 6;
    // Colors from blue to yellow to green to brown to gray to white
                            // water,                      sand,                       grass,                        dirt,                       rock,                   snow
    vec4 colors[numberOfTextures] = vec4[numberOfTextures](vec4(0.32, 0.33, 0.19, 1.0), vec4(0.58, 0.53, 0.27, 1.0), vec4(0.38, 0.45, 0.23, 1.0), vec4(0.25, 0.21, 0.11, 1) , vec4(0.5, 0.5, 0.5, 1.0), vec4(0.9, 0.9, 0.9, 1.0));
    //vec2 normTexCoord = 400 * TexCoord;// 400  rotateUV(TexCoord, Rotation_);
    vec2 Resolution = vec2(400, 400);
    // convert degrees to radians
    float angle = (Rotation_ * 3.14159265) / 180.0;
    float sin_factor = sin(angle);
    float cos_factor = cos(angle);
    vec2 uv = TexCoord_ + vec2(Perlin_/1000, Perlin_/1000);
    // clamp to [0, 1]
    uv = clamp(uv, 0.0, 1.0);
    vec2 normTexCoord = terrainTiling * uv * mat2(cos_factor, sin_factor, -sin_factor, cos_factor);

    

    vec4 colors2[numberOfTextures] = vec4[numberOfTextures](texture(waterTexture, normTexCoord), texture(sandTexture, normTexCoord), texture(grassTexture, normTexCoord),texture(dirtTexture, normTexCoord), texture(material.specular, normTexCoord), texture(material.specular, normTexCoord));
    float locations[numberOfTextures] = float[numberOfTextures](0.1, 0.11, 0.12, 0.26, 0.5, 0.63);
    vec4 color = LinearGradient(h, colors, locations);
    vec4 color2 = LinearGradient(h, colors2, locations);
    vec4 col = color2 * color * ( (1.0 - shadow));//(heightCol + vec4(0,0, 0.2-heightCol.z,1))

    float slope = (texture(slopeMap, TexCoord_+Perlin_/300).y/2);
    //if slope is too steep, don't render
    float slopeVal = length(slope);
    vec4 slopeCol = vec4(slopeVal, slopeVal, slopeVal, 1.0);
    vec4 underWater = vec4(1-slopeVal/2, 1-slopeVal/2, 1-slopeVal/2, 1.0);
    //underWater = max(underWater, 0.2);

    vec4 terrainColor = (col + clamp(col*underWater, 0.0, 1.0));

    return terrainColor;
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