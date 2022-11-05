from __future__ import annotations
from core.component import Component
import glm

class Transform(Component):
        
    def __init__(self):
        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1,1,1)
    
    @classmethod
    def RotatePoint(self, rotation, point):
        rotationQuat = glm.quat(glm.radians(rotation))
        return rotationQuat * point
    
    @property
    def up(self):
        up = glm.vec3(0, 1, 0)
        right = glm.normalize(glm.cross(up, self.rotation))
        up = glm.cross(self.rotation, right)
        return up
        
        
    @property
    def right(self):
        up = glm.vec3(0, 1, 0)
        right = glm.normalize(glm.cross(up, self.rotation))
        return right    
    
    def GetPoseMatrix(self):
        idty = glm.mat4(1.0)
        scale = glm.scale(idty, self.scale)
        rotationQuat = glm.quat(glm.radians(self.rotation))
        rotation = glm.mat4(rotationQuat)
        trans = glm.translate(idty, self.position) 
        poseMtx = trans * rotation * scale
        return poseMtx
    
        
        