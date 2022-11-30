#version 440 core
#extension GL_EXT_geometry_shader4 : enable 

layout (triangles) in;
layout (triangle_strip, max_vertices=3) out; 

in vec3 FragPos_;
in vec3 ourColor_;
in vec2 TexCoord_;
in vec3 Normal_;
in vec4 FragPosLightSpace_;
in mat4 MVP_;

out vec3 FragPos;
out vec3 ourColor;
out vec2 TexCoord;
out vec3 Normal;
out vec4 FragPosLightSpace;
out mat4 MVP;

void main() {
    gl_Position = gl_in[0].gl_Position + vec4(-0.1, 0.0, 0.0, 0.0); 
    EmitVertex();

    gl_Position = gl_in[0].gl_Position + vec4( 0.1, 0.0, 0.0, 0.0);
    EmitVertex();
    
    EndPrimitive();

    FragPos = FragPos_;
    ourColor = ourColor_;
    TexCoord = TexCoord_;
    Normal = Normal_;
    FragPosLightSpace = FragPosLightSpace_;
    MVP = MVP_;
}