import glm
import OpenGL.GL as gl

from core.util import GetRootPathDir


class Shader:
    '''
    The shader class is used to load and compile shaders from files
    '''
    def __init__(
        self, 
        vertexShaderName: str, 
        fragmentShaderName: str, 
        geomShaderName: str = "", 
        tessControlShaderName:str = "", 
        tessEvalShaderName:str = "", 
        shaderRootPath = "resources/shaders/"
        ):
        # Get shader code
        with open(f'{GetRootPathDir()}/{shaderRootPath}{fragmentShaderName}.glsl', "r") as file:
            f_shader:str = file.read()
        with open(f'{GetRootPathDir()}/{shaderRootPath}{vertexShaderName}.glsl', "r") as file:
            v_shader:str = file.read()
            
        if geomShaderName != "":
            with open(f'{GetRootPathDir()}/{shaderRootPath}{geomShaderName}.glsl', "r") as file:
                g_shader:str = file.read()
                
        if tessControlShaderName != "":
            with open(f'{GetRootPathDir()}/{shaderRootPath}{tessControlShaderName}.glsl', "r") as file:
                t_c_shader:str = file.read()
        
        if tessEvalShaderName != "":
            with open(f'{GetRootPathDir()}/{shaderRootPath}{tessEvalShaderName}.glsl', "r") as file:
                t_e_shader:str = file.read()
        
        # Create object 
        vertexShaderID = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fragShaderID = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        if geomShaderName != "":
            geometryShaderID = gl.glCreateShader(gl.GL_GEOMETRY_SHADER)
        if tessControlShaderName != "":
            tessControlShaderID = gl.glCreateShader(gl.GL_TESS_CONTROL_SHADER)
        if tessEvalShaderName != "":
            tessEvalShaderID = gl.glCreateShader(gl.GL_TESS_EVALUATION_SHADER)
        
        # Compile vertex shader
        gl.glShaderSource(vertexShaderID, v_shader)
        gl.glCompileShader(vertexShaderID)
        # print compile errors if any
        if not gl.glGetShaderiv(vertexShaderID, gl.GL_COMPILE_STATUS):
            msg = gl.glGetShaderInfoLog(vertexShaderID)
            print("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n", msg)
            
        # Compile fragment shader
        gl.glShaderSource(fragShaderID, f_shader)
        gl.glCompileShader(fragShaderID)
        # print compile errors if any
        if not gl.glGetShaderiv(fragShaderID, gl.GL_COMPILE_STATUS):
            msg = gl.glGetShaderInfoLog(fragShaderID)
            print("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n", msg)
            
        # Compile goemerty shader
        if geomShaderName != "":
            gl.glShaderSource(geometryShaderID, g_shader)
            gl.glCompileShader(geometryShaderID)
            # print compile errors if any
            if not gl.glGetShaderiv(geometryShaderID, gl.GL_COMPILE_STATUS):
                msg = gl.glGetShaderInfoLog(geometryShaderID)
                print("ERROR::SHADER::GEOMETRY::COMPILATION_FAILED\n", msg)
                
        # Compile tesselation control shader
        if tessControlShaderName != "":
            gl.glShaderSource(tessControlShaderID, t_c_shader)
            gl.glCompileShader(tessControlShaderID)
            # print compile errors if any
            if not gl.glGetShaderiv(tessControlShaderID, gl.GL_COMPILE_STATUS):
                msg = gl.glGetShaderInfoLog(tessControlShaderID)
                print("ERROR::SHADER::TESS_CONTROL::COMPILATION_FAILED\n", msg)
            
         # Compile tesselation evaluation shader    
        if tessEvalShaderName != "":
            gl.glShaderSource(tessEvalShaderID, t_e_shader)
            gl.glCompileShader(tessEvalShaderID)
            # print compile errors if any
            if not gl.glGetShaderiv(tessEvalShaderID, gl.GL_COMPILE_STATUS):
                msg = gl.glGetShaderInfoLog(tessEvalShaderID)
                print("ERROR::SHADER::TESS_EVAL::COMPILATION_FAILED\n", msg)
                
        # bind shaders to program object
        
        # Create program object
        shaderProgramID = gl.glCreateProgram()
        
        # attach shaders to program
        gl.glAttachShader(shaderProgramID, vertexShaderID)
        gl.glAttachShader(shaderProgramID, fragShaderID)
        if geomShaderName != "":
            gl.glAttachShader(shaderProgramID, geometryShaderID)
        if tessControlShaderName != "":
            gl.glAttachShader(shaderProgramID, tessControlShaderID)   
        if tessEvalShaderName != "":
            gl.glAttachShader(shaderProgramID, tessEvalShaderID)   
            
        # links and package everthing into the program (ins and outs of shaders matched)
        gl.glLinkProgram(shaderProgramID)
        
        # Delete shaders since we have already linked them to the program
        gl.glDeleteShader(vertexShaderID)
        gl.glDeleteShader(fragShaderID) 
        if geomShaderName != "":
            gl.glDeleteShader(geometryShaderID) 
        if tessControlShaderName != "":
            gl.glDeleteShader(tessControlShaderID)
        if tessEvalShaderName != "":
            gl.glDeleteShader(tessEvalShaderID)
        
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
        gl.glUniform1f(gl.glGetUniformLocation(self.shaderProgramID, attribName), value)
        
    def setMat4(self, attribName:str, value):
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.shaderProgramID, attribName), 1, gl.GL_FALSE, glm.value_ptr(value))

    def setVec3(self, attribName:str, value):
        gl.glUniform3fv(gl.glGetUniformLocation(self.shaderProgramID, attribName), 1, value)
        
    def setVec4(self, attribName:str, value):
        gl.glUniform4fv(gl.glGetUniformLocation(self.shaderProgramID, attribName), 1, value)