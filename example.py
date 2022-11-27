import pygame as pg
from pygame.locals import *
import numpy as np
import OpenGL.GL as gl
import ctypes
import glm
import time

FLOAT_SIZE = 4

vertices=[
    #vPos  color  uv
    0,0,0, 1,0,1, 1,1,#0
    1,0,0, 1,0,0, 1,0,#1
    0,1,0, 0,1,1, 0,0,#2
    1,1,0, 1,0,1, 0,1,#3
    0,0,1, 1,1,1, 1,1,#4
    1,0,1, 1,1,1, 1,0,#5
    0,1,1, 1,1,1, 0,0,#6
    1,1,1, 1,1,1, 0,1,#7
    ]

triangles = [
    #bottom face
    2,0,3,
    3,0,1,
    #top face
    4,6,5,
    5,6,7,
    #side faces
    #1
    0,4,1,
    1,4,5,
    #2
    1,5,3,
    3,5,7,
    
    #3
    3,7,2,
    2,7,6,
    
    #4
    2,6,0,
    0,6,4
]

class Texture:
    def __init__(self, path:str):
        self.width, self.height = 0, 0
        self.rawTexData = None
        self.textureID = 0
        try:
            # load image
            image = pg.image.load(f'{path}')
            image = pg.transform.flip(image, False, False)
            self.width, self.height = image.get_rect().size
            self.rawTexData = pg.image.tostring(image, "RGBA")
        except:
            print(f"ERROR: Could not load texture at {path}")
            return

        self.CreateTexture()
        
    def CreateTexture(self):
        if not self.rawTexData:
            return
        
        self.textureID = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureID)
        
        # set the texture wrapping/filtering options
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)	
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.rawTexData)
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        
    def use(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureID)
        
    def free(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

class Shader:
    
    def __init__(self, vertexString: str, fragmentString: str):
        # Get shader code
        f_shader:str = fragmentString
        v_shader:str = vertexString
        
        # Create object 
        vertexShaderID = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fragShaderID = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        
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
        gl.glUniform1fv(gl.glGetUniformLocation(self.shaderProgramID, attribName), 1, value)
        
    def setMat4(self, attribName:str, value):
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.shaderProgramID, attribName), 1, gl.GL_FALSE, value)

    def setVec3(self, attribName:str, value):
        gl.glUniform3fv(gl.glGetUniformLocation(self.shaderProgramID, attribName), 1, value)
        
    def setVec4(self, attribName:str, value):
        gl.glUniform4fv(gl.glGetUniformLocation(self.shaderProgramID, attribName), 1, value)

def ToArr(vectorList, datatype):
    return np.array(vectorList, datatype)

def createGPUData():
    vertexShader = """
        #version 330 core
        layout (location = 0) in vec3 aPos;
        layout (location = 1) in vec3 aColor;
        layout (location = 2) in vec2 aTexCoord;


        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main()
        {
            gl_Position = projection * view * model * vec4(aPos, 1.0);
        }
    """
    
    fragmentShader = """
    #version 330 core

    void main()
    {             
        gl_FragColor = vec4(1,1,1,1);
    } 
    """
    shader = Shader(vertexShader, fragmentShader)
    texture = Texture("textures/cat.png")
    
    # We need tio tell opengl how to proc4ess vertex data and how to send that
    # data to the shaders
    
    # generate VAO so we don't have to copy our VBO every time and set attribs
    vaoID = gl.glGenVertexArrays(1)
    # Generate VBO Object with ID
    vboID = gl.glGenBuffers(1)
    # Generate EBO
    eboID = gl.glGenBuffers(1)
    
    # Bind VAO so now all the VBO stuff we do below will be stored inside this VAO
    gl.glBindVertexArray(vaoID)
    
    # Bind vbo to GL_ARRAY_BUFFER object
    # # Now all calls we make that affect  GL_ARRAY_BUFFER will
    # configure the currently bound buffer
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vboID)
    # Copy vertex data into current GL_ARRAY_BUFFER which is the object we binded
    gl.glBufferData(gl.GL_ARRAY_BUFFER, ToArr(vertices, np.float32), gl.GL_STATIC_DRAW)
    
    # Bind ebo to GL_ELEMENT_ARRAY_BUFFER object
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, eboID)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, ToArr(triangles, np.uint32), gl.GL_STATIC_DRAW)

    
    # index index of atrib to be used by shader
    # size- number of components in the attribute
    # type- datatype of attribute 
    # normalised - whether attribs should be normalised
    # stride - offset to jump to next attributes
    # pointer- starting index of first attribute
    
    #vertex position
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8*FLOAT_SIZE, ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)
    
    #vertex color
    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 8*FLOAT_SIZE, ctypes.c_void_p(3*FLOAT_SIZE))
    gl.glEnableVertexAttribArray(1)
    
    #vertex uv
    gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8*FLOAT_SIZE, ctypes.c_void_p(6*FLOAT_SIZE))
    gl.glEnableVertexAttribArray(2)
    
    # Now when we want to render we canm just do 
    # gl.glUseProgram(shaderProgramID)
    # gl.glBindVertexArray(vaoID)
    # someOpenGLDrawStuff()
    
    # Unbind VAO so it isn't accidently modified
    gl.glBindVertexArray(0) 
    
    # Unbind VBO as it isn't needed in context anymore
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0) 
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0) 
    
    
    return shader, texture, vaoID
    
    
deltaTime = 0
r = 0
def render(shader: Shader, texture: Texture, vaoID):
    global deltaTime
    global r
    current_time = time.time()
    gl.glClearColor(0, 0, 0, 1)
    # Clear color and depth buffers
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    
    # Render stuff inside here
    
    # Set shader and VAO to be used to render calls 
    # Every drawing call after this point will use the prgram and it's shaders
    # and also all the VBOs defined in the VAO
    shader.use()
    texture.use()
    r += deltaTime * 15
    idty = glm.mat4(1.0)
    trans = glm.rotate(idty, glm.radians(r), glm.vec3(1,1,1))
    model = glm.scale(trans, glm.vec3(0.5,0.5,0.5))
    
    view = glm.translate(idty, glm.vec3(0.0, 0.0, -3.0)) 
    
    projection = glm.perspective(glm.radians(95.0), 800.0 / 600.0, 0.1, 100.0)
    
    shader.setMat4("model", glm.value_ptr(model))
    shader.setMat4("view", glm.value_ptr(view))
    shader.setMat4("projection", glm.value_ptr(projection))
    
    gl.glBindVertexArray(vaoID)
    # Actually draw the stuff!
    #gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(vertices))
    gl.glDrawElements(gl.GL_TRIANGLES, len(vertices), gl.GL_UNSIGNED_INT, None)
    
    
    # Flip frame buffers since we are using double buffering
    pg.display.flip()
    
    shader.free()
    texture.free()
    deltaTime = time.time() - current_time

def main():
    
    # Set the caption of the screen
    pg.display.set_caption('My Window')
    
    # Variable to keep our game loop running
    running = True
    
    window_size = [800, 600]
    
    # Enable double frame buffering and tell pygame to use opengl context
    pg.display.set_mode([window_size[0], window_size[1]], DOUBLEBUF|OPENGL)
    
    # tell opengl we need a renderering viewport of 800 by 600
    # open gl beind the scenes maps normalised vieewport points i.e. 0 to 1 to pixel coords i.e. 304px to 783px
    # we are telling it to map 0 to 1 to 0 to 800 and 0 to 600 in x and y respectively
    gl.glViewport(0, 0, window_size[0], window_size[1])
    
    # Set background colour for opengl
    gl.glClearColor(0, 0, 0, 1)
    
     # Enable depth test to let opengl store depth buffer
    gl.glEnable(gl.GL_DEPTH_TEST)
    
    # tell opengl that it should expect vertex arrays
    gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
    
    # Passes if the fragment's depth value is less than the stored depth value.
    gl.glDepthFunc(gl.GL_LESS)
    
    #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    
    # Create data fro gpu to redner
    # You can say this represents all the data needed to render
    # one object.
    shader, texture, vaoID = createGPUData()
    
    # game loop
    while running:
        
        render(shader, texture, vaoID)
    # for loop through the event queue  
        for event in pg.event.get():
            # Check for QUIT event      
            if event.type == pg.QUIT:
                running = False
    

if __name__ == "__main__":
    main()