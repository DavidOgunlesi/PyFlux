from __future__ import annotations
import time
import core.gametime as gametime
import OpenGL.GL as gl
import pygame as pg
from pygame.locals import *
from core.scene import Scene
import core.input as input
import core.eventsystem as eventsystem
class Runtime:
    def __init__(self, scene: Scene = None):
        self.scene = scene
        self.deltaTime = 0
        self.active = False
    
    def InitRuntime(self):
        if self.scene == None:
            print("Error initialisinf runtime. Scene cannot be null.")
            return
        
        self.scene.StartScene()
        self.active = True
    
    def SetScene(self, scene: Scene):
        self.scene = scene
        self.deltaTime = 0
        self.active = False
    
    def QuitEvent(self, _, __):
        self.active = False
        
    def test(self):
        print("SADASD")
    def Run(self):
        if self.scene == None:
            print("Error initialisinf runtime. Scene cannot be null.")
            return
        if not self.active:
            print("Runtime not Initialised. Initialise before calling Run().")
            return
        
        while self.active:
            gl.glClearColor(0, 0, 0, 1)
            gl.glStencilMask(0xff)
            # Clear color and depth buffers
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
            current_time = time.time()
            
            eventsystem.pollEvent(pg.QUIT, self.QuitEvent)
            
            if input.GetKeyDown(pg.K_ESCAPE):
                self.active = False
            
            self.scene.UpdateScene()
            
            eventsystem.ExecuteEvents()
            gametime.deltaTime = time.time() - current_time
            # Flip frame buffers since we are using double buffering
            pg.display.flip()
    