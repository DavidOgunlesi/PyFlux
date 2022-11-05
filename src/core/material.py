from __future__ import annotations
from typing import TYPE_CHECKING, List, Type
import OpenGL.GL as gl
from core.shader import Shader
from core.texture import Texture

class Material:
    def __init__(self, shader: Shader, diffuseTex:Texture = None, specularTex:Texture = None):
        self.shader = shader
        self.diffuseTex = diffuseTex
        self.specularTex = specularTex
    
    def SetProperties(self):
        self.shader.setInt("material.diffuse", 0)
        self.shader.setInt("material.specular", 1)
        self.shader.setFloat("material.shininess", 32.0)
    
    def use(self):
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.diffuseTex.textureID)
        
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.specularTex.textureID)
        
    def free(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        
    