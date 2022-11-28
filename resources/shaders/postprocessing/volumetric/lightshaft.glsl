#version 330 core
  
in vec2 TexCoords;

uniform sampler2D tex;
uniform sampler2D occulusionMap;
uniform vec3 LightPos;
int NUM_SAMPLES = 100;

vec4 LightShaftColor(vec3 ScreenLightPos, sampler2D samplerImage, float Density, float Weight, float Decay, float Exposure);


void main()
{
    //Covert light position in world space to NDC
    vec4 lightPos = vec4(LightPos, 1.0);
    lightPos = lightPos / lightPos.w;
    lightPos = lightPos * 0.5 + 0.5;
    lightPos.y = 1.0 - lightPos.y;
    lightPos.x = lightPos.x * 2.0 - 1.0;
    lightPos.y = lightPos.y * 2.0 - 1.0;
    lightPos.z = lightPos.z * 2.0 - 1.0;
    lightPos.w = 1.0;
    
    gl_FragColor = texture(occulusionMap, TexCoords) ;//+ LightShaftColor(vec3(LightPos), occulusionMap, 1, 1, 0.5, 0.5);
} 



vec4 LightShaftColor(vec3 ScreenLightPos, sampler2D samplerImage, float Density, float Weight, float Decay, float Exposure) {   
    // Calculate vector from pixel to light source in screen space.    
    vec2 deltaTexCoord = (TexCoords - ScreenLightPos.xy);   
    // Divide by number of samples and scale by control factor.   
    deltaTexCoord *= 1.0 / NUM_SAMPLES * Density;   
    // Store initial sample.    
    vec3 color = vec3(texture(samplerImage, TexCoords));   
    // Set up illumination decay factor.    
    float illuminationDecay = 1.0;   
    vec2 texCoord = TexCoords;
    // Evaluate summation from Equation 3 NUM_SAMPLES iterations.    
    for (int i = 0; i < NUM_SAMPLES; i++)   
    {     
        // Step sample location along ray.    
        texCoord -= deltaTexCoord;     
        // Retrieve sample at new location.    
        vec3 sample = vec3(texture(samplerImage, texCoord));    
        // Apply sample attenuation scale/decay factors.     
        sample *= illuminationDecay * Weight;     
        // Accumulate combined color.     
        color += sample;    
        // Update exponential decay factor.     
        illuminationDecay *= Decay;   
    }   

    // Output final color with a further scale control factor.    
    return vec4( color * Exposure, 1); 
} 