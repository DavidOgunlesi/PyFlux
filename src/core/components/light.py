from __future__ import annotations
from typing import TYPE_CHECKING
from core.component import Component
import glm

if TYPE_CHECKING:
    from scene import Scene
    from core.object import Object
    from components.transform import Transform

class Light(Component):
    
    def __init__(self):
        self.ambient = glm.vec3(0.2, 0.2, 0.2)
        self.diffuse = glm.vec3(1, 1, 1)
        self.specular = glm.vec3(1, 1, 1)
    
    def Init(self, parent: Object, scene: Scene, transform: Transform):
        super().Init(parent, scene, transform)
        self.scene.lightCollection.addLight(self)
    
    def SetColor(self, color: glm.vec3):
        self.diffuse = color
        
    def SetSpecular(self, color: glm.vec3):
        self.specular = color
        
    def SetSpecular(self, color: glm.vec3):
        self.ambient = color
        
class DirectionalLight(Light):
    def __init__(self):
        Light.__init__(self)
        self.direction = glm.vec3(0, 0, 0)
        
    def SetDirection(self, dir: glm.vec3):
        self.direction = dir
        
class PointLight(Light):
    def __init__(self):
        Light.__init__(self)
        self.constant = 1.0
        self.linear = 0.09
        self.quadratic = 0.032
        
class SpotLight(DirectionalLight, PointLight):
    def __init__(self):
        DirectionalLight.__init__(self)
        PointLight.__init__(self)
        self.cutOff = glm.cos(glm.radians(12.5))
        self.outerCutOff = glm.cos(glm.radians(15.5))
        
    def SetCutOff(self, degrees:float):
        self.cutOff = glm.cos(glm.radians(degrees))
    
    def SetOuterCutOff(self, degrees:float):
        self.outerCutOff = glm.cos(glm.radians(degrees))
        