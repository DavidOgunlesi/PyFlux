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
import math
import core.gametime as gm
import core.input as input
import core.eventsystem as eventsystem

class Camera(Component):
    def __init__(self):
        self.viewMatrix = glm.mat4(1.0)
        self.projection = None
        self.SetPerspective()
        self.i = 0
        self.cameraSpeed = 10
        
    def Start(self):
        radius = 3
        self.i += gm.deltaTime * 5
        camX = math.sin(self.i) * radius
        camZ = math.cos(self.i) * radius
        
        self.transform.position = glm.vec3(camX, camX, camZ)
    
    def Update(self):
        # radius = 3
        # self.i += gm.deltaTime * 5
        # camX = math.sin(self.i) * radius
        # camZ = math.cos(self.i) * radius
        
        # self.transform.position = glm.vec3(camX, camX, camZ)
        #self.DoCameraInputs()
        # eventsystem.pollEvent(pg.KEYDOWN, self.DoCameraInputs)
        
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.transform.position += glm.vec3(0,0, -self.cameraSpeed) * gm.deltaTime
        if keys[pg.K_s]:
            self.transform.position += glm.vec3(0,0, self.cameraSpeed) * gm.deltaTime
        if keys[pg.K_a]:
            self.transform.position += glm.vec3(-self.cameraSpeed, 0, 0) * gm.deltaTime
        if keys[pg.K_d]:
            self.transform.position += glm.vec3(self.cameraSpeed, 0, 0) * gm.deltaTime
        self.viewMatrix = self.GetViewMatrix()
    
    def SetPerspective(self, fov: float = 95, near:float = 0.1, far:float = 100):
        self.projection = glm.perspective(glm.radians(fov), 800.0 / 600.0, near, far)
        
    def SetOrthographic(self, left:float = 0, right:float = 800, bottom: float = 600 ,top:float = 100, near:float = 0.1, far:float = 100):
        self.projection = glm.ortho(left, right, bottom, top, near, far)
    
    def GetViewMatrix(self):
        idty = glm.mat4(1.0)
        # view matrix is negation of transform position because 
        # we have to move the scene forward to simulate camera moving backwards
        
        cameraTarg = glm.vec3()
        #origin to pos
        cameraDirection = glm.normalize(self.transform.position - cameraTarg)
        
        up = glm.vec3(0,1,0)   
        cameraRight = glm.normalize(glm.cross(up, cameraDirection))     
        cameraUp = glm.cross(cameraDirection, cameraRight)
        
        #return glm.lookAt(self.transform.position, cameraTarg, cameraUp)
        
        idty = glm.mat4(1.0)
        return glm.translate(idty, -self.transform.position) 

    