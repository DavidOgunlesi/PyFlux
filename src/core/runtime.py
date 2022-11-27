from __future__ import annotations
import time
import core.gametime as gametime
import OpenGL.GL as gl
import pygame as pg
from pygame.locals import *
from core.scene import Scene
import core.input as input
import core.eventsystem as eventsystem
from core.shader import Shader
import core.globals as GLOBAL
from core.components.mesh import Mesh
from typing import List
import glm

class Runtime:
    
    class RenderJob:
        def __init__(self) -> None:
            self.mesh: Mesh = None
    
    def __init__(self):
        self.deltaTime = 0
        self.active = False
        self.depthMapFBO = 0
        self.depthMap = 0
        self.scene = None
        self.renderTexMesh: Mesh = None
        self.renderQueue: List[Mesh] = []
        GLOBAL.CURRENTRENDERCONTEXT = self
    
    def InitRuntime(self):
        if self.scene == None:
            print("Error initialisinf runtime. Scene cannot be null.")
            return
        self.depthMapFBO, self.depthMap = self.GenDepthMap()
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
            current_time = time.time()
            
            eventsystem.pollEvent(pg.QUIT, self.QuitEvent)
            
            if input.GetKeyDown(pg.K_ESCAPE):
                self.active = False
                
            self.RenderShadowMap()
            # Render QUAD
            self.RenderScene()
            
            eventsystem.ExecuteEvents()
            gametime.deltaTime = time.time() - current_time
            # Flip frame buffers since we are using double buffering
            pg.display.flip()
            

    def QueueRender(self, mesh: Mesh):
        self.renderQueue.append(mesh)
    
    def RenderData(self):
        # sort jobs by distance to camera so that transparent stuff works
        self.renderQueue.sort(key=lambda m: m.GetDistanceToCamera(), reverse=True)
        for job in self.renderQueue:
            job.Render(shadowMap = self.depthMap)
            
        self.renderQueue.clear()
        
    def GetLightSpaceTransform(self):
        near_plane = 1.0 
        far_plane = 7.5
        lightProjection = glm.ortho(-10.0, 10.0, -10.0, 10.0, near_plane, far_plane)
        
        lightView = glm.lookAt(glm.vec3(10,0, 0), glm.vec3(0,0,0), glm.vec3(0,1,0))  
        lightSpaceMatrix = lightProjection * lightView
        return lightSpaceMatrix
        
    def RenderShadowMap(self):  
        SHADOW_WIDTH = 1024
        SHADOW_HEIGHT = 1024
        # 1. first render to depth map
        gl.glViewport(0, 0, SHADOW_WIDTH, SHADOW_HEIGHT)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.depthMapFBO)
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT) 

        # Rendering from normal camera perspective rn
        shader = Shader("env/lightmap/simpledepth_vert","env/lightmap/null_frag")
        #shader = Shader("vertex","fragment")
        GLOBAL.GLOBAL_RENDERSHADER = shader
        self.scene.UpdateScene()
        self.RenderData()

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        GLOBAL.GLOBAL_RENDERSHADER = None
         
    def RenderScene(self):
        gl.glViewport(0, 0, 800, 600)
        # gl.glClearColor(0, 0, 0, 1)
        gl.glStencilMask(0xff)
        # Clear color and depth buffers
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
        self.scene.UpdateScene() 

        #self.renderTexMesh.Render(True, self.depthMap)

        self.RenderData()
        
    def GenDepthMap(self):
        depthMapFBO = gl.glGenFramebuffers(1); 
        SHADOW_WIDTH = 1024
        SHADOW_HEIGHT = 1024

        # Create a 2D texture that we'll use as the framebuffer's depth buffer
        depthMap = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, depthMap)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_DEPTH_COMPONENT, SHADOW_WIDTH, SHADOW_HEIGHT, 0, gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT, None) # Try Zeo
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
          
        # Attach it as the framebuffer's depth buffer:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, depthMapFBO)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_TEXTURE_2D, depthMap, 0)
        
        # Explicitly tell OpenGL we're not going to render any color data
        gl.glDrawBuffer(gl.GL_NONE)
        gl.glReadBuffer(gl.GL_NONE)
        
        if(gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE):
            print("SUCCESS")
        
        
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        return depthMapFBO, depthMap
    