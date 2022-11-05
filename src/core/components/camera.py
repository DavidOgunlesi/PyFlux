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
from core.components.transform import Transform

class Camera(Component):
    def __init__(self):
        self.viewMatrix = glm.mat4(1.0)
        self.projection = None
        self.SetPerspective()
        self.cameraSpeed = 10
        self.sensitivity = 1
        self.yaw = 90
        self.pitch = 0
        self.cameraFront = glm.vec3()
        self.cameraUp = glm.vec3()
        
    def Start(self):
        self.transform.position = glm.vec3(0, 0, -5)
    
    def Update(self):
        self.DoCameraInputs()
        self.DoMouseLook()
        self.viewMatrix = self.GetViewMatrix()
    
    def DoMouseLook(self):
        x,y = pg.mouse.get_rel()
        
        self.yaw += x * self.sensitivity
        self.pitch -= y * self.sensitivity
        
        if self.pitch > 89:
            self.pitch =  89
        if self.pitch < -89:
            self.pitch = -89
        
        if self.yaw < 0:
            self.yaw += 360
        if self.yaw > 360:
            self.yaw -= 360
        
        direction = glm.vec3()
        direction.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        direction.y = math.sin(glm.radians(self.pitch))
        direction.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        self.cameraFront = glm.normalize(direction)
        
    
    def DoCameraInputs(self):
        if input.GetKeyPressed(pg.K_w):
            self.transform.position +=  self.cameraSpeed * self.cameraFront * gm.deltaTime
        if input.GetKeyPressed(pg.K_s):
            self.transform.position -=  self.cameraSpeed * self.cameraFront * gm.deltaTime
        if input.GetKeyPressed(pg.K_a):
            self.transform.position -=  self.cameraSpeed * glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * gm.deltaTime
        if input.GetKeyPressed(pg.K_d):
            self.transform.position += self.cameraSpeed * glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * gm.deltaTime
        if input.GetKeyPressed(pg.K_SPACE):
            right = glm.normalize(glm.cross(self.cameraUp, self.cameraFront))
            up = glm.cross(self.cameraFront, right)
            self.transform.position +=  self.cameraSpeed * up * gm.deltaTime
        if input.GetKeyPressed(pg.K_LCTRL):
            right = glm.normalize(glm.cross(self.cameraUp, self.cameraFront))
            up = glm.cross(self.cameraFront, right)
            self.transform.position -=  self.cameraSpeed * up * gm.deltaTime
    
    def SetPerspective(self, fov: float = 95, near:float = 0.1, far:float = 100):
        self.projection = glm.perspective(glm.radians(fov), 800.0 / 600.0, near, far)
        
    def SetOrthographic(self, left:float = 0, right:float = 800, bottom: float = 600 ,top:float = 100, near:float = 0.1, far:float = 100):
        self.projection = glm.ortho(left, right, bottom, top, near, far)
    
    def GetViewMatrix(self):
        #origin to pos
        #cameraDirection = glm.normalize(self.transform.position - cameraTarg)
        #cameraRight = glm.normalize(glm.cross(up, cameraDirection))   
        up = glm.vec3(0,1,0)     
        self.cameraUp = up 
        #self.transform.rotation = glm.lookAt(glm.vec3(), self.cameraFront, up) * self.transform.rotation
        return glm.lookAt(self.transform.position, self.transform.position + self.cameraFront, self.cameraUp)
        
       # return self.transform.GetPoseMatrix(self.transform.PoseOrder.RTS) 

    