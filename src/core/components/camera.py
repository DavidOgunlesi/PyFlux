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
    def Copy(self) -> Component:
        c = Camera()
        c.viewMatrix = self.viewMatrix
        c.projection = self.projection
        c.cameraSpeed = self.cameraSpeed
        c.sensitivity = self.sensitivity
        c.yaw = self.yaw
        c.pitch = self.pitch
        c.cameraFront = self.cameraFront
        c.cameraUp = self.cameraUp
        c.fov = self.fov
        c.zoomFactor = self.zoomFactor
        c.zoomSpeed = self.zoomSpeed
        c.near = self.near
        c.far = self.far
        c.left = self.left
        c.right = self.right
        c.bottom = self.bottom
        c.top = self.top
        c.projType = self.projType
        return c
        
    def __init__(self):
        Component.__init__(self)
        self.viewMatrix = glm.mat4(1.0)
        self.projection = None
        self.cameraSpeed = 10
        self.sensitivity = 1
        self.yaw = 90
        self.pitch = 0
        self.cameraFront = glm.vec3()
        self.cameraUp = glm.vec3()
        self.fov = 90
        self.zoomFactor = 1
        self.zoomSpeed = 50
        self.near = 0.1
        self.far = 100000
        self.left:float = 0
        self.right:float = 8
        self.bottom: float = 0
        self.top:float = 6
        self.projType = 0
        
    def Start(self):
        self.transform.position = glm.vec3(0, 0, -5)
    
    def Update(self):
        if self.projType == 0:
            self.projection = glm.perspective(glm.radians(self.fov*self.zoomFactor), 800.0 / 600.0, self.near, self.far)
        else:
            self.projection = glm.ortho(self.left*self.zoomFactor, self.right*self.zoomFactor, self.bottom*self.zoomFactor, self.top*self.zoomFactor, self.near, self.far)
            glm.ortho(0.0, 4.0, 0.0, 3.0, 0.1, 100.0)
            
        self.DoCameraMovement()
        self.DoMouseLook()
        self.DoCameraZoom()
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
    
    def DoCameraZoom(self):
        _,sy = input.GetMouseWheel()
        self.cameraSpeed += sy * self.cameraSpeed * gm.deltaTime * 100
        self.cameraSpeed = min(max(self.cameraSpeed, 1), 10000)
    
    def DoCameraMovement(self):
        if input.GetKeyPressed(pg.K_w) and self.projType == 0:
            self.transform.position +=  self.cameraSpeed * self.cameraFront * gm.deltaTime
        if input.GetKeyPressed(pg.K_s) and self.projType == 0:
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
        self.fov = fov
        self.near = near
        self.far = far
        self.projType = 0
        
    def SetOrthographic(self, left:float = 0, right:float = 8, bottom: float = 0 ,top:float = 6, near:float = 0.1, far:float = 100):
        self.near = near
        self.far = far
        self.left = left, 
        self.right = right, 
        self.bottom = bottom,
        self.top = top
        self.projType = 1

    
    def GetViewMatrix(self):
        #origin to pos
        #cameraDirection = glm.normalize(self.transform.position - cameraTarg)
        #cameraRight = glm.normalize(glm.cross(up, cameraDirection))   
        up = glm.vec3(0,1,0)     
        self.cameraUp = up
        return glm.lookAt(self.transform.position, self.transform.position + self.cameraFront, self.cameraUp)

    