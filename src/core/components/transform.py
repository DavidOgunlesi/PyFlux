from __future__ import annotations
from core.component import Component
import glm
import math
import numpy as np
class Transform(Component):
        
    def __init__(self):
        self.position = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1,1,1)
        #self._rotationQuat = glm.quat(glm.radians(glm.vec3(0, 0, 0)))
        self._rotationMat4 = glm.mat4(1)
        self.overridePM = None
        
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
        # dir = point - self.position
        # v1 = dir
        
        # direction = glm.vec3()
        # direction.x = math.cos(glm.radians(self.rotation.x)) * math.cos(glm.radians(self.rotation.y))
        # direction.y = math.sin(glm.radians(self.rotation.y))
        # direction.z = math.sin(glm.radians(self.rotation.x)) * math.cos(glm.radians(self.rotation.y))
        
        # v2 = direction
        
        # a = glm.cross(v1, v2)
        # q = glm.quat(a.x,a.y,a.z, 0)
        # q.w = math.sqrt((glm.length(v1)**2) * (glm.length(v2)**2)) + glm.dot(v1, v2)
        # q = glm.normalize(q)
        
        # self._rotationMat4 = glm.mat4(self.GetRotBetween(dir, self.up)) #= glm.degrees(glm.eulerAngles(q))
        # z = glm.normalize(dir)
        # sideVec = glm.cross(dir, self.up)
        # un = glm.cross(dir, sideVec) 
        # m = glm.mat3(0)
        # m[0] = glm.normalize(dir)
        # m[1] = glm.normalize(un)
        # m[2] = glm.normalize(sideVec)
        # # y = glm.normalize(glm.cross( z, x )) # y = z cross x 
        # m = glm.mat4(1)
        # m[0] = x
        # m[1] = y
        # m[2] = z
        # quat = glm.quat_cast(m)
        # self.rotation = glm.degrees(glm.eulerAngles(quat))
        dir = glm.normalize(point - self.position)
        up = -np.sign(dir.z) * self.up
        right = np.sign(dir.z) * self.right
        self.rotation = glm.vec3(glm.dot(up, dir)*90,glm.dot(right, dir)*90,0)
    
    def LookAtOLD(self, point):
       
        #dir = glm.normalize(point - self.position)
        #rot = self.AnglesFromVectors(dir, glm.vec3(0,1,0))
        #self.rotation = glm.vec3(rot.x, rot.y, rot.z)
        #direction = glm.normalize(point - self.position)
        #lookAt = glm.lookAt(self.transform.position, self.transform.position-point, glm.vec3(0,1,0))
        #self.rotation = glm.degrees(glm.eulerAngles(glm.quat_cast(lookAt)))
        # if (self.rotation.z >= 90):
        #     self.rotation.x += 180
        #     self.rotation.y = 180 - self.rotation.y
        #     self.rotation.z += 180
        return
        dirProj = point - self.position
        dirProj = glm.normalize(glm.vec3(dirProj.x, 0, dirProj.z))
        lookAt = glm.vec3(0, 0, 1)
        upAux = glm.cross(lookAt, dirProj)
        angleCosine = glm.dot(lookAt, dirProj)
        
        if ((angleCosine < 0.99990) and (angleCosine > -0.9999)):
            rot = glm.rotate(self._rotationMat4, glm.acos(angleCosine)*180/math.pi, upAux) 
            self._rotationMat4 = rot#glm.eulerAngles(glm.quat_cast(rot))
            
        dir = glm.normalize(point - self.position)
        angleCosine = glm.dot(dirProj, dir)
        if angleCosine < 0.99990 and angleCosine > -0.9999:
            if dir.y < 0:
                rot = glm.rotate(self._rotationMat4, glm.acos(angleCosine)*180/math.pi, glm.vec3(1,0,0)) 
                self._rotationMat4 *= rot#glm.eulerAngles(glm.quat_cast(rot))
            else:
                rot = glm.rotate(self._rotationMat4, glm.acos(angleCosine)*180/math.pi, glm.vec3(-1,0,0))
                self._rotationMat4 *= rot#glm.eulerAngles(glm.quat_cast(rot))
         
    
    @property
    def up(self):
        return glm.vec3(0, 1, 0)
        
        
    @property
    def right(self):
        return glm.vec3(1, 0, 0)    
    
    def GetPoseMatrix(self):
        idty = glm.mat4(1.0)
        scale = glm.scale(idty, self.scale)
        rotation = self._rotationMat4
        trans = glm.translate(idty, self.position) 
        poseMtx =  trans *  rotation   * scale 
        return poseMtx
    
    # def GetPoseMatrix(self):
    #     if self.overridePM == None:
    #         self.overridePM = self.GetTruePoseMatrix()
    #     return self.overridePM
    
    # def OverridePoseMatrix(self, mat):
    #     self.overridePM = mat
    
        
        