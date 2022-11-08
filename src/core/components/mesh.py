from __future__ import annotations
import ctypes
import time

import glm
import numpy as np
import OpenGL.GL as gl
import pygame as pg
from core.constants import FLOAT_SIZE

from pygame.locals import *
from typing import List
from core.component import Component
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.material import Material
    
class Mesh(Component):
    def __init__(self, type: int, **kwargs):
        self.vertices = kwargs["vertices"]
        self.offset = glm.vec3(0,0,0)
        if type == 0:
            self.EasyConstructMesh(kwargs)
        else:
            self.ConstructMesh(kwargs)
    
    def EasyConstructMesh(self, kwargs):
        vertices = kwargs["vertices"]
        triangles = kwargs["triangles"]
        colors = kwargs["colors"]
        uvs = kwargs["uvs"]
        #vertices = self.NormalizeMeshCentre(vertices)
        normals = self.CalculateNormals(vertices, triangles)
        self.vertexData = self.GenerateVertexAttribDataCollectionOLD(vertices, triangles, colors, uvs, normals)
        self.faceData = list(range(0, len(triangles)))
        self.VAO = self.GenerateVAO()
    
    def ConstructMesh(self, kwargs):
        vertices = kwargs["vertices"]
        triangles = kwargs["triangles"]
        uvs = kwargs["uvs"]
        normals = kwargs["normals"]
        
        if uvs == []:
            uvs = [[1,1]]*(len(vertices))
            
        #vertices = self.NormalizeMeshCentre(vertices)
        self.vertexData = self.GenerateVertexAttribDataCollection(vertices, uvs, normals)
        self.faceData = np.array(triangles, dtype=np.int32).flatten().tolist()
        self.VAO = self.GenerateVAO()
    
    def Start(self):
        return super().Start()
    
    def Update(self):
        self.Render()
    
    
    def SetMaterial(self, material:Material):
        self.material = material
    
    def GetMeshCentre(self):
        return np.average(self.vertices, axis=0)
        
                
    def ToArr(self, vectorList, datatype):
        return np.array(vectorList, datatype)
    
    def GenerateVertexAttribDataCollectionOLD(self, vertices, triangles, colors, uvs, normals) :
        vertexData = []
        for idx, vert_index in enumerate(triangles):
            data = np.concatenate((vertices[vert_index], [1,1,1] ,uvs[idx], normals[idx]), axis=0)
            vertexData.append(data)
            
        return vertexData
    
    def GenerateVertexAttribDataCollection(self, vertices, uvs, normals) :
        vertexData = []
        for i in range(0, len(vertices)):
            data = np.concatenate((vertices[i][0:3], [1,1,1] ,uvs[i][0:2], normals[i][0:3]), axis=0)
            vertexData.append(data)
        return vertexData
    
    def GenerateVertexAttribDataCollection_(self, vertices, triangles, colors, uvs, normals) :
        vertexData = []
        #print(triangles[0])
        triangles = np.array(triangles, dtype=np.int32)
        for face in triangles:
            for vert_index in face:
                data = np.concatenate((vertices[vert_index], [1,1,1] ,uvs[vert_index], normals[vert_index]), axis=0)
                vertexData.append(data.tolist())
        return vertexData
    
    def CalculateNormals(self, vertices, triangles):
        """
        Calculate normals automatically from triangles an vertices. 
        Not recommended for complex meshes!
        """
        normals = []
        # loop through all faces
        triIdx = 0
        
        while triIdx != len(triangles):
            # Get face vertices
            rV = glm.vec3(vertices[triangles[triIdx]])
            aV = glm.vec3(vertices[triangles[triIdx+1]])
            bV= glm.vec3(vertices[triangles[triIdx+2]])
            
            # Get both face vectors
            fV1 = aV - rV
            fV2 = bV - rV
            
            # Calculate cross product and use as normal
            crossVector = glm.cross(fV2, fV1)
            normals.append(crossVector.to_list())
            normals.append(crossVector.to_list())
            normals.append(crossVector.to_list())
            triIdx+=3
        return normals
    
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
        
        numOfAttribComponents = 11
        #vertex position
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, numOfAttribComponents*FLOAT_SIZE, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)
        
        #vertex color
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, numOfAttribComponents*FLOAT_SIZE, ctypes.c_void_p(3*FLOAT_SIZE))
        gl.glEnableVertexAttribArray(1)
        
        #vertex uv
        gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, numOfAttribComponents*FLOAT_SIZE, ctypes.c_void_p(6*FLOAT_SIZE))
        gl.glEnableVertexAttribArray(2)
        
        #vertex normals
        gl.glVertexAttribPointer(3, 3, gl.GL_FLOAT, gl.GL_FALSE, numOfAttribComponents*FLOAT_SIZE, ctypes.c_void_p(8*FLOAT_SIZE))
        gl.glEnableVertexAttribArray(3)
        
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
        self.material.use()
        self.material.SetProperties(self.scene.lightCollection)
        self.transform.pivot = self.offset
        modelMtx = self.transform.GetPoseMatrix()
        viewMtx = self.scene.mainCamera.viewMatrix
        projection = self.scene.mainCamera.projection
        
        self.material.shader.setMat4("model", glm.value_ptr(modelMtx))
        self.material.shader.setMat4("view", glm.value_ptr(viewMtx))
        self.material.shader.setMat4("projection", glm.value_ptr(projection))
        self.material.shader.setVec3("cameraPos", self.scene.mainCamera.transform.position.to_list())
        
        
        
        self.material.shader.setVec3("dirLight.ambient",  self.scene.mainLight.ambient.to_list())
        self.material.shader.setVec3("dirLight.diffuse",  self.scene.mainLight.diffuse.to_list())
        self.material.shader.setVec3("dirLight.specular", self.scene.mainLight.specular.to_list())
        self.material.shader.setVec3("dirLight.direction", self.scene.mainLight.direction.to_list())
        
        
        gl.glBindVertexArray(self.VAO)
        # Actually draw the stuff!
        #gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(vertices))
        #gl.glPointSize(10);   
        gl.glDrawElements(gl.GL_TRIANGLES, len(self.faceData), gl.GL_UNSIGNED_INT, None)
        
        self.material.shader.free()
        self.material.free()

    