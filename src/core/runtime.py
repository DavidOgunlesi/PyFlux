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
from core.components.postprocessing import PostProcessing
class Runtime:
    
    class RenderJob:
        def __init__(self) -> None:
            self.mesh: Mesh = None
    
    def __init__(self):
        self.deltaTime = 0
        self.active = False
        self.depthMapFBO = 0
        self.depthMap = 0
        self.preoccpassFBO = 0
        self.preoccpass = 0
        self.scene = None
        self.renderTexMesh: Mesh = None
        self.renderQueue: List[Mesh] = []
        GLOBAL.CURRENTRENDERCONTEXT = self
        self.SHADOW_WIDTH = 4096
        self.SHADOW_HEIGHT = 4096 #1024
        self.postProcessor: PostProcessing = None
        
    
    def InitRuntime(self):
        if self.scene == None:
            print("Error initialisinf runtime. Scene cannot be null.")
            return
        self.depthMapFBO, self.depthMap = self.GenDepthMap()
        self.preoccpassFBO, self.preoccpass = self.postProcessor.GenEffectBuffer()
        self.postProcessor.InitialiseEffects(self.scene)
        self.scene.StartScene()
        self.active = True
    
    def SetScene(self, scene: Scene):
        self.scene = scene
        self.deltaTime = 0
        self.active = False
    
    def AddPostProcessing(self, postProcessing: PostProcessing):
        self.postProcessor = postProcessing
    
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
        print("Running Runtime")
        while self.active:
            current_time = time.time()
            
            eventsystem.pollEvent(pg.QUIT, self.QuitEvent)
            
            if input.GetKeyDown(pg.K_ESCAPE):
                self.active = False
                
             
            # self.OcculusionPrePass() TODO: Fix this
            self.scene.UpdateScene()
            self.RenderShadowMap()
            self.scene.UpdateScene()
            # Render QUAD
            if self.postProcessor != None and len(self.postProcessor.stack) != 0:
                self.RenderSceneWithPostProcessing()
            else:
                self.RenderSceneWithoutPostProcessing()
                
            # self.renderTexMesh.Render()
            
            eventsystem.ExecuteEvents()
            gametime.deltaTime = time.time() - current_time
            gametime.time += gametime.deltaTime
            # Flip frame buffers since we are using double buffering
            pg.display.flip()
            

    def QueueRender(self, mesh: Mesh):
        self.renderQueue.append(mesh)
    
    def RenderData(self, shadowPass):
        # sort jobs by distance to camera so that transparent stuff works
        self.renderQueue.sort(key=lambda m: m.GetDistanceToCamera(), reverse=True)
        for job in self.renderQueue:
            if not shadowPass and job.renderPass:
                job.Render(shadowMap = self.depthMap)
            elif job.castShadows and job.renderPass:    
                #job.FlipCullMode() # Flip to prevent peter panning
                job.Render()
                #job.FlipCullMode()
                
        self.renderQueue.clear()
        
    def GetLightSpaceTransform(self):
        near_plane = 0
        far_plane = 75
        lightProjection = glm.ortho(-80.0, 80.0, -80.0, 80.0, near_plane, far_plane)
        
        lightView = glm.lookAt(self.scene.mainLight.transform.position, glm.vec3(0,0,0), glm.vec3(0,1,0))  
        lightSpaceMatrix = lightProjection * lightView
        return lightSpaceMatrix
        
    def OcculusionPrePass(self):
        # 1. first render to depth map
        gl.glViewport(0, 0, 800, 600)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.preoccpassFBO)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)

        shader = Shader("preoccpass/vert","preoccpass/frag")
        
        GLOBAL.GLOBAL_RENDERSHADER = shader
        self.RenderData(False)

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        GLOBAL.GLOBAL_RENDERSHADER = None
        
    def RenderShadowMap(self):  
        # 1. first render to depth map
        gl.glViewport(0, 0, self.SHADOW_WIDTH, self.SHADOW_HEIGHT)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.depthMapFBO)
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT) 

        # Rendering from normal camera perspective rn
        shader = Shader("env/lightmap/simpledepth_vert","env/lightmap/null_frag")
        
        GLOBAL.GLOBAL_RENDERSHADER = shader
        #self.scene.UpdateScene()
        self.RenderData(True)

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        GLOBAL.GLOBAL_RENDERSHADER = None
    
    def RenderSceneWithPostProcessing(self):
        gl.glViewport(0, 0, 800, 600)
        gl.glStencilMask(0xff)
        # Clear color and depth buffers
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)

        # If post processing effects is an odd number, add defualt effect to the end
        
        if len(self.postProcessor.stack) % 2 != 0:
            self.postProcessor.AddPostProcessingEffect(PostProcessing.DefaultEffect())
            
        #1) Render scene to post process framebuffer 1
        self.postProcessor.useFBO()
        self.RenderData(False)
        for effect in self.postProcessor.stack:
            #Render Quad with post processing effects with current FBO as texture
            # but render to other FBO
            currentTex = self.postProcessor.GetTextureID()
            self.postProcessor.PingPong() # pingpong so we can render to other FBO
            
            # If we are at the last effect, render to screen instead of FBO
            if effect == self.postProcessor.stack[-1]:
                # Free the FBOs so we can render to the screen normally
                self.postProcessor.freeFBO()
            else:
                self.postProcessor.useFBO()
                
            self.postProcessor.RenderQuad(currentTex, effect)
        
        self.postProcessor.freeFBO()
         
    def RenderSceneWithoutPostProcessing(self):
        gl.glViewport(0, 0, 800, 600)
        gl.glStencilMask(0xff)
        # Clear color and depth buffers
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
        self.RenderData(False)
        
    def GenDepthMap(self):
        depthMapFBO = gl.glGenFramebuffers(1);

        # Create a 2D texture that we'll use as the framebuffer's depth buffer
        depthMap = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, depthMap)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_DEPTH_COMPONENT, self.SHADOW_WIDTH, self.SHADOW_HEIGHT, 0, gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT, None) # Try Zeo
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_BORDER)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_BORDER)
        borderColor = glm.vec4(1, 1, 1, 1)
        gl.glTexParameterfv(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_BORDER_COLOR, borderColor.to_list());  
          
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
    
    