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


class Camera(Component):
    def __init__(self):
        pass
    
    def Start(self):
        return super().Start()
    
    def Update(self):
        pass
    
    def GetViewMatrix(self):
        idty = glm.mat4(1.0)
        # view matrix is negation of transform position because 
        # we have to move the scene forward to simulate camera moving backwards
        cameraPos = glm.translate(idty, -self.transform.position) 
        cameraTarg = glm.vec3()
        #origin to pos
        cameraDirection = glm.normalise(cameraPos - cameraTarg)
        
        up = glm.vec3(0,1,0)   
        cameraRight = glm.normalise(glm.cross(up, cameraDirection))     
        

    