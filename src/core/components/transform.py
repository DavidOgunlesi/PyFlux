from __future__ import annotations
from typing import ClassVar
from core.component import Component
import glm
import math
import numpy as np

class Transform(Component):
    def Copy(self) -> Component:
        c = Transform()
        c.position = self.position
        c.scale = self.scale
        c._rotationMat4 = self._rotationMat4
        c.pivot = self.pivot
        return c
    def __init__(self):
        Component.__init__(self)
        self.position = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1,1,1)
        self._rotationMat4 = glm.mat4(1)
        self.pivot = glm.vec3(0, 0, 0)
        
    @property
    def rotation(self):
        return glm.degrees(glm.eulerAngles(glm.quat_cast(self._rotationMat4)))
    
    @rotation.setter
    def rotation(self, rotation):
        rotationQuat = glm.quat(glm.radians(rotation))
        self._rotationMat4 = glm.mat4(rotationQuat)
    
    @classmethod
    def RotatePoint(self, rotation, point):
        rotationQuat = glm.quat(glm.radians(rotation))
        return rotationQuat * point
    
    def orthogonal(self, v):
        x = abs(v.x)
        y = abs(v.y)
        z = abs(v.z)
        xAxis = glm.vec3(1,0,0)
        yAxis = glm.vec3(0,1,0)
        zAxis = glm.vec3(0,0,1)
        other = (xAxis if x < z else zAxis) if x < y else (yAxis if y < z else zAxis)
        return glm.cross(v, other)
    
    def GetRotBetween(self, u, v):
        k_cos_theta = glm.dot(u, v)
        k = math.sqrt(glm.length(u) + glm.length(v))
        
        if k_cos_theta / k == -1:
            no = glm.normalize(self.orthogonal(u))
            return glm.quat(0, no.x, no.y, no.z)
        
        c = glm.cross(u,v)
        return glm.normalize(glm.quat(k_cos_theta + k, c.x, c.y, c.z))
    
    def LookAt(self, point):
        dir = glm.normalize(point - self.position)
        up = -np.sign(dir.z) * self.up
        right = np.sign(dir.z) * self.right
        self.rotation = glm.vec3(glm.dot(up, dir)*90,glm.dot(right, dir)*90,0)
    
    def TransformPoint(self, point):
        return self.GetPoseMatrix() * point
    
    def InverseTransformPoint(self, point):
        return glm.inverse(self.GetPoseMatrix()) * point
    
    @property
    def up(self):
        return glm.vec3(0, 1, 0)
        
        
    @property
    def right(self):
        return glm.vec3(1, 0, 0)    
    
    def GetPoseMatrix(self, translation = None, rotation = None, scale = None):
        if translation is None:
            translation = self.position
            
        if rotation != None:
            rotationQuat = glm.quat(glm.radians(rotation))
            rotation = glm.mat4(rotationQuat)
        else:
            rotation = self._rotationMat4
            
        if scale is None:
            scale = self.scale
            
        idty = glm.mat4(1.0)
        scale = glm.scale(idty, scale)
        pivotTrans = glm.translate(idty, self.pivot) 
        trans = glm.translate(idty, translation) 
        poseMtx =  trans *  rotation  * scale * pivotTrans
        return poseMtx

    
        
        