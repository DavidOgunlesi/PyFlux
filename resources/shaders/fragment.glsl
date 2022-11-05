#version 330

in vec3 FragPos;
in vec3 ourColor;
in vec2 TexCoord;
in vec3 Normal;

uniform sampler2D ourTexture;
uniform vec3 lightColor;
uniform vec3 lightPos;
uniform vec3 cameraPos;
uniform vec3 ambientColor;

void main()
{
    float ambientStrength = 1;
    float specularStrength = 1;

    //Lighting calculation
    vec3 norm = normalize(Normal);
     //Very costly, better to calculate on CPU and pass into here using uniform!
     //vec3 norm = mat3(transposeFunc(inverseFunc(gl_ModelViewProjectionMatrix))) * normalize(NormalCoord); 
    vec3 lightDir = normalize(lightPos - FragPos);  

     //Get diffuse color from dot product
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // Specular lighting
    vec3 viewDir = normalize(cameraPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);

    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;  

    // Factor in ambient light (shadhow color) and specular
    vec4 texColor = texture(ourTexture, TexCoord);

    vec3 sum = ambientColor + diffuse + specular;
    vec4 result = vec4(sum, 1.0) * texColor;
    gl_FragColor = vec4(result);
} 