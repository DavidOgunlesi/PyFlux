#version 330

in vec3 FragPos;
in vec3 ourColor;
in vec2 TexCoord;
in vec3 Normal;
in vec4 FragPosLightSpace;

in float Height;
in float Rotation;
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

float ShadowCalculation(DirLight light, vec3 normal, vec4 fragPosLightSpace);
float CalculateSpecComponent(vec3 lightDir, vec3 normal, vec3 viewDir);
vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir, float shadow);  
vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir, float shadow);  
vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir, float shadow);  


vec4 LinearGradient(float value, vec4[4] colors, float[4] locations) {
    if (value <= locations[0]) {
        return colors[0];
    }
    if (value >= locations[locations.length() - 1]) {
        return colors[colors.length() - 1];
    }
    for (int i = 0; i < locations.length() - 1; i++) {
        if (value >= locations[i] && value <= locations[i + 1]) {
            float t = (value - locations[i]) / (locations[i + 1] - locations[i]);
            return mix(colors[i], colors[i + 1], t);
        }
    }
    return vec4(0.0, 0.0, 0.0, 1.0);
}

vec2 rotateUV(vec2 uv, float rotation)
{
    float mid = 0.5;
    return vec2(
        cos(rotation) * (uv.x - mid) + sin(rotation) * (uv.y - mid) + mid,
        cos(rotation) * (uv.y - mid) - sin(rotation) * (uv.x - mid) + mid
    );
}

void main()
{
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(cameraPos - FragPos);
    //Shadow
    float shadow = ShadowCalculation(dirLight, norm, FragPosLightSpace); 
    // phase 1: Directional lighting
    vec3 result = CalcDirLight(dirLight, norm, viewDir, shadow);
    // phase 2: Point lights
    for(int i = 0; i < NR_POINT_LIGHTS; i++){   
        if (pointLights[i].set == false){
            continue;
        }else{
            result += CalcPointLight(pointLights[i], norm, FragPos, viewDir, shadow);    
        } 
    }   
    // phase 3: Spot lights
    for(int i = 0; i < NR_SPOT_LIGHTS; i++){
        if (spotLights[i].set == false){
            continue;
        }else{
            result += CalcSpotLight(spotLights[i], norm, FragPos, viewDir, shadow);
        }
    }
    vec4 tex = texture(material.diffuse, TexCoord);

    // Environment mapping
    vec3 envReflect = reflect(viewDir, norm);

    //Refraction
    float ratio = 1.00 / 4.52;
    vec3 envRefract = refract(viewDir, norm, ratio);

    vec3 R = envReflect;
    R *= vec3(1, -1, 1);

    float h = (Height + 16)/64.0f;
	vec4 heightCol = vec4(h, h, h, 1.0);
    
    // Colors from blue to yellow to green to brown to gray to white
    vec4 colors[4] = vec4[4](vec4(0.0, 0.0, 1.0, 1.0), vec4(1.0, 1.0, 0.0, 1.0), vec4(0.0, 1.0, 0.0, 1.0), vec4(0.5, 0.5, 0.5, 1.0));
    //vec2 normTexCoord = 400 * TexCoord;// 400  rotateUV(TexCoord, Rotation);
    vec2 Resolution = vec2(400, 400);
    // convert degrees to radians
    float angle = (Rotation * 3.14159265) / 180.0;
    float sin_factor = sin(angle);
    float cos_factor = cos(angle);
    vec2 normTexCoord = 400 * TexCoord * mat2(cos_factor, sin_factor, -sin_factor, cos_factor);
    vec4 tiledVal = texture(material.diffuse, normTexCoord);
    vec4 colors2[4] = vec4[4](texture(material.diffuse, normTexCoord), tiledVal, tiledVal, tiledVal);
    float locations[4] = float[4](0.0, 0.25, 0.5, 1.0);
    vec4 color = LinearGradient(h, colors, locations);
    vec4 color2 = LinearGradient(h, colors2, locations);
    gl_FragColor = color * color2;
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

vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir, float shadow){
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

    return (ambient + (1.0 - shadow) * (diffuse + specular));
}

vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir, float shadow){
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

    return  (ambient + (1.0 - shadow) * (diffuse + specular));
}

vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir, float shadow){
    
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

   return  (ambient + (1.0 - shadow) * (diffuse + specular));
}