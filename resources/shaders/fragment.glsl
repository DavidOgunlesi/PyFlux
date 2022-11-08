#version 330

in vec3 FragPos;
in vec3 ourColor;
in vec2 TexCoord;
in vec3 Normal;

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
    float shininess;
}; 

uniform Material material;

uniform DirLight dirLight; 

#define NR_POINT_LIGHTS 4  
uniform PointLight pointLights[NR_POINT_LIGHTS];
#define NR_SPOT_LIGHTS 4  
uniform SpotLight spotLights[NR_SPOT_LIGHTS];   

uniform samplerCube skybox;

float CalculateSpecComponent(vec3 lightDir, vec3 normal, vec3 viewDir);
vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir);  
vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir);  
vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir);  

void main()
{
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(cameraPos - FragPos);

    // phase 1: Directional lighting
    vec3 result = CalcDirLight(dirLight, norm, viewDir);
    // phase 2: Point lights
    for(int i = 0; i < NR_POINT_LIGHTS; i++){   
        if (pointLights[i].set == false){
            continue;
        }else{
            result += CalcPointLight(pointLights[i], norm, FragPos, viewDir);    
        } 
    }   
    // phase 3: Spot lights
    for(int i = 0; i < NR_SPOT_LIGHTS; i++){
        if (spotLights[i].set == false){
            continue;
        }else{
            result += CalcSpotLight(spotLights[i], norm, FragPos, viewDir);
        }
    }
    vec4 tex = texture(material.diffuse, TexCoord);

    // Environment mapping
    vec3 envReflect = reflect(viewDir, norm);

    //Refraction
    float ratio = 1.00 / 4.52;
    vec3 envRefract = refract(viewDir, norm, ratio);

    vec3 R = envRefract;
    R *= vec3(1, -1, 1);
    vec4 skyboxContribution = vec4(texture(skybox, R).rgb, 1.0) * (1-dot(norm, viewDir))  * texture(material.specular, TexCoord);
    gl_FragColor = vec4(result, tex.a) + skyboxContribution;
} 

//Blinn Phong specular
float CalculateSpecComponent(vec3 lightDir, vec3 normal, vec3 viewDir){
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), material.shininess);
   //vec3 reflectDir = reflect(-lightDir, normal);  
   //float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
   return spec;
}

vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir){
    // diffuse 
    vec3 lightDir = normalize(light.direction);
    float diff = max(dot(normal, lightDir), 0.0);
    
    // specular
    //vec3 reflectDir = reflect(-lightDir, normal);  
    //float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    float spec = CalculateSpecComponent(lightDir, normal, viewDir);

    // Combine
    vec3 ambient  = light.ambient * vec3(texture(material.diffuse, TexCoord));
    vec3 diffuse  = light.diffuse * diff * vec3(texture(material.diffuse, TexCoord)); 
    vec3 specular = light.specular * spec * vec3(texture(material.specular, TexCoord)); 

    return (ambient +  diffuse + specular);
}

vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir){
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

    vec3 ambient = light.ambient * vec3(texture(material.diffuse, TexCoord));
    vec3 diffuse = light.diffuse * diff * vec3(texture(material.diffuse, TexCoord)); 
    vec3 specular = light.specular * (spec *  vec3(texture(material.specular, TexCoord)));  
    
    ambient  *= attenuation; 
    diffuse  *= attenuation;
    specular *= attenuation; 

    return (ambient +  diffuse + specular);
}

vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir){
    
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
    
    vec3 ambient = light.ambient * vec3(texture(material.diffuse, TexCoord));
    vec3 diffuse = light.diffuse * diff * vec3(texture(material.diffuse, TexCoord)); 
    vec3 specular = light.specular * (spec *  vec3(texture(material.specular, TexCoord))); 

    ambient  *= attenuation; 
    diffuse  *= attenuation;
    specular *= attenuation; 

    diffuse  *= intensity;
    specular *= intensity; 

   return (ambient +  diffuse + specular);
}