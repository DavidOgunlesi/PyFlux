import OpenGL.GL as gl
from core.util import GetRootPathDir

class Shader:
    
    def __init__(self, vertexShaderName: str, fragmentShaderName: str, shaderRootPath = "resources/shaders/"):
        # Get shader code
        with open(f'{GetRootPathDir()}/{shaderRootPath}{fragmentShaderName}.glsl', "r") as file:
            f_shader:str = file.read()
        with open(f'{GetRootPathDir()}/{shaderRootPath}{vertexShaderName}.glsl', "r") as file:
            v_shader:str = file.read()
        
        # Create object 
        vertexShaderID = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fragShaderID = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        
        # Compile vertex shader
        gl.glShaderSource(vertexShaderID, v_shader)
        gl.glCompileShader(vertexShaderID)
        
        # Compile fragment shader
        gl.glShaderSource(fragShaderID, f_shader)
        gl.glCompileShader(fragShaderID)
        
        # bind shaders to program object
        
        # Create program object
        shaderProgramID = gl.glCreateProgram()
        
        # attach shaders to program
        gl.glAttachShader(shaderProgramID, vertexShaderID)
        gl.glAttachShader(shaderProgramID, fragShaderID)
        
        # links and package everthing into the program (ins and outs of shaders matched)
        gl.glLinkProgram(shaderProgramID)
        
        # Delete shaders since we have already linked them to the program
        gl.glDeleteShader(vertexShaderID)
        gl.glDeleteShader(fragShaderID) 
        
        self.shaderProgramID = shaderProgramID
        
    def use(self):
        gl.glUseProgram(self.shaderProgramID)
     
    def free(self):
         gl.glUseProgram(0)
         
    def setInt(self, attribName:str, value:int):
        gl.glUniform1i(gl.glGetUniformLocation(self.shaderProgramID, attribName), value)
        
    def setBool(self, attribName:str, value:bool):
        gl.glUniform1i(gl.glGetUniformLocation(self.shaderProgramID, attribName), value)
        
    def setFloat(self, attribName:str, value:float):
        gl.glUniform1fv(gl.glGetUniformLocation(self.shaderProgramID, attribName), value)
        
    def setMat4(self, attribName:str, value):
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.shaderProgramID, attribName), 1, gl.GL_FALSE, value)

        