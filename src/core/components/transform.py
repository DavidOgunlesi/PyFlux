from core.component import Component
import glm

class Transform(Component):
    
    def __init__(self):
        self.position = glm.vec3()
        self.rotation = glm.vec3()
        self.scale = glm.vec3(1,1,1)
        
    def GetPoseMatrix(self):
        idty = glm.mat4(1.0)
        scale = glm.scale(idty, self.scale)
        rotationQuat = glm.quat(glm.radians(self.rotation))
        rotation = glm.mat4(rotationQuat)
        trans = glm.translate(idty, self.position) 
        poseMtx = trans * rotation * scale
        return poseMtx
    
        
        