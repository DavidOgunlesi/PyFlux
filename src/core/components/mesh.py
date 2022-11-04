import ctypes
import time

import glm
import numpy as np
import OpenGL.GL as gl
import pygame as pg
from core.constants import FLOAT_SIZE
from core.material import Material
from pygame.locals import *

from core.component import Component


class Mesh(Component):
    def __init__(self, vertexData: np.array, faceData: np.array):
        self.vertexData = vertexData
        self.faceData = faceData
        self.VAO = self.GenerateVAO()
    
    def Start(self):
        return super().Start()
    
    def Update(self):
        self.Render()
    
    
    def SetMaterial(self, material:Material):
        self.material = material
    
    def ToArr(self, vectorList, datatype):
        return np.array(vectorList, datatype)
    
    def GenerateVAO(self):
        
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
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.ToArr(self.vertexData, np.float32), gl.GL_STATIC_DRAW)
        
        # Bind ebo to GL_ELEMENT_ARRAY_BUFFER object
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, eboID)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.ToArr(self.faceData, np.uint32), gl.GL_STATIC_DRAW)
        
        #vertex position
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8*FLOAT_SIZE, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)
        
        #vertex color
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 8*FLOAT_SIZE, ctypes.c_void_p(3*FLOAT_SIZE))
        gl.glEnableVertexAttribArray(1)
        
        #vertex uv
        gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8*FLOAT_SIZE, ctypes.c_void_p(6*FLOAT_SIZE))
        gl.glEnableVertexAttribArray(2)
        
        # Unbind VAO so it isn't accidently modified
        gl.glBindVertexArray(0) 
        
        # Unbind VBO as it isn't needed in context anymore
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0) 
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0) 
        
        return vaoID
    
    def Render(self):
        # Set shader and VAO to be used to render calls 
        # Every drawing call after this point will use the prgram and it's shaders
        # and also all the VBOs defined in the VAO
        self.material.shader.use()
        self.material.texture.use()
        
        modelMtx = self.transform.GetPoseMatrix()
        viewMtx = self.scene.mainCamera.viewMatrix
        projection = self.scene.mainCamera.projection
        
        
        self.material.shader.setMat4("model", glm.value_ptr(modelMtx))
        self.material.shader.setMat4("view", glm.value_ptr(viewMtx))
        self.material.shader.setMat4("projection", glm.value_ptr(projection))
        
        gl.glBindVertexArray(self.VAO)
        # Actually draw the stuff!
        #gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(vertices))
        gl.glDrawElements(gl.GL_TRIANGLES, len(self.vertexData), gl.GL_UNSIGNED_INT, None)
        
        self.material.shader.free()
        self.material.texture.free()

    