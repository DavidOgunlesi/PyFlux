from __future__ import annotations
from typing import TYPE_CHECKING, List, Type
import OpenGL.GL as gl
from core.shader import Shader
from core.texture import Texture

from core.components.light import SpotLight, PointLight 
import glm

if TYPE_CHECKING:
    from core.collections.light import LightCollection
class Material:
    def __init__(self, shader: Shader, diffuseTex:Texture = None, specularTex:Texture = None):
        self.shader = shader
        self.diffuseTex = diffuseTex or Texture("textures/noTex.png")
        self.specularTex = specularTex or Texture("textures/noTex.png")
    
    def SetProperties(self, lightCollection: LightCollection):
        self.shader.setInt("material.diffuse", 0)
        self.shader.setInt("material.specular", 1)
        self.shader.setFloat("material.shininess", 32.0)
        
        for idx, light in enumerate(lightCollection.lights):
            if type(light) == SpotLight:
                l: SpotLight = light
                self.shader.setBool(f"spotLights[{idx}].set", True)
                self.shader.setVec3(f"spotLights[{idx}].position", l.transform.position.to_list())
                self.shader.setVec3(f"spotLights[{idx}].direction", l.direction.to_list())
                
                self.shader.setVec3(f"spotLights[{idx}].ambient",  l.ambient.to_list())
                self.shader.setVec3(f"spotLights[{idx}].diffuse",  l.diffuse.to_list())
                self.shader.setVec3(f"spotLights[{idx}].specular", l.specular.to_list())
                
                self.shader.setFloat(f"spotLights[{idx}].cutOff", l.cutOff)
                self.shader.setFloat(f"spotLights[{idx}].outerCutOff", l.outerCutOff)
                
                self.shader.setFloat(f"spotLights[{idx}].constant", l.constant)
                self.shader.setFloat(f"spotLights[{idx}].linear", l.linear)
                self.shader.setFloat(f"spotLights[{idx}].quadratic", l.quadratic)
                
            elif type(light) == PointLight:
                l: PointLight = light
                self.shader.setBool(f"pointLights[{idx}].set", True)
                self.shader.setVec3(f"pointLights[{idx}].position", l.transform.position.to_list())
                
                self.shader.setVec3(f"pointLights[{idx}].ambient",  l.ambient.to_list())
                self.shader.setVec3(f"pointLights[{idx}].diffuse",  l.diffuse.to_list())
                self.shader.setVec3(f"pointLights[{idx}].specular", l.specular.to_list())              
                
                self.shader.setFloat(f"pointLights[{idx}].constant", l.constant)
                self.shader.setFloat(f"pointLights[{idx}].linear", l.linear)
                self.shader.setFloat(f"pointLights[{idx}].quadratic", l.quadratic)
                
    
    def use(self):
        if self.diffuseTex:
            gl.glActiveTexture(gl.GL_TEXTURE0)
            self.diffuseTex.use()
            
        if self.specularTex:
            gl.glActiveTexture(gl.GL_TEXTURE1)
            self.specularTex.use()
    

        
    def free(self):
        #gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        if self.diffuseTex:
            gl.glActiveTexture(gl.GL_TEXTURE0)
            self.diffuseTex.free()
            
        if self.specularTex:
            gl.glActiveTexture(gl.GL_TEXTURE1)
            self.specularTex.free()
        
    