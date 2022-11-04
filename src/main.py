import ctypes
import time

import glm
import numpy as np
import OpenGL.GL as gl
import pygame as pg
from core.components.mesh import Mesh
from core.components.transform import Transform
from core.material import Material
from core.object import Object
from pygame.locals import *
from core.runtime import Runtime
from core.scene import Scene
from core.shader import Shader
from core.texture import Texture

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

def ToArr(vectorList, datatype):
    return np.array(vectorList, datatype)

def createGPUData():
    
    shader = Shader("vertex", "fragment")
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

def ConstructScene():
    scene = Scene()
    
    testObj = Object()
    mesh = Mesh(vertices, triangles)
    mesh.SetMaterial(Material(Shader("vertex", "fragment"), Texture("textures/cat.png")))
    testObj.AddComponent(mesh)
    scene.Instantiate(testObj)
    
    obj = scene.Instantiate(testObj)
    obj.transform.position = glm.vec3(1,0,0)
    
    
    return scene

def main():
    
    # Set the caption of the screen
    pg.display.set_caption('My Window')
    
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
    
    runtime:Runtime = Runtime()
    
    scene = ConstructScene()
    
    runtime.SetScene(scene)
    runtime.InitRuntime()
    runtime.Run()

if __name__ == "__main__":
    main()