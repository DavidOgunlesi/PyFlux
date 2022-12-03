from __future__ import annotations
from typing import TYPE_CHECKING, List
from core.texture import Texture, InternalTexture
from core.component import Component
from core.components.mesh import Mesh
from core.primitives import PRIMITIVE
from core.shader import Shader
from core.object import Object
from core.material import Material
import OpenGL.GL as gl
import glm
import core.gametime as gametime
import core.globals as GLOBAL

if TYPE_CHECKING:
    from core.scene import Scene

class PostProcessing(Component):
    '''
    Post processing component handles the post processing effect stack
    '''
    class Effect:
        def __init__(self):
            self.shader: Shader = None
            
        def PassUniforms(self, shader: Shader):
            pass    
        
    class DefaultEffect(Effect):
        def __init__(self):
            #self.shader = Shader("misc/postprocessing/default/vert", "misc/postprocessing/default/frag")
            self.shader = Shader("misc/rendertexture/vert", "postprocessing/default")
    
    class Grayscale(Effect):
        def __init__(self):
            self.shader = Shader("misc/rendertexture/vert", "postprocessing/grayscale")
    
    class Inversion(Effect):
        def __init__(self):
            self.shader = Shader("misc/rendertexture/vert", "postprocessing/inversion")
            
    class FilmGrain(Effect):
        def __init__(self, intensity:float, skipAmount = 1):
            self.shader = Shader("misc/rendertexture/vert", "postprocessing/filmgrain")
            self.intensity = intensity
            self.__skip = 0
            self.skipAmount = skipAmount
            
        def PassUniforms(self, shader: Shader):
            if self.__skip % self.skipAmount == 0:
                shader.setFloat("time", gametime.time)
            self.__skip += 1
            shader.setFloat("intensity", self.intensity)
            pass
    
    class Vignette(Effect):
        def __init__(self, power:float):
            self.shader = Shader("misc/rendertexture/vert", "postprocessing/vignette")
            self.power = 0.25
        def PassUniforms(self, shader: Shader):
            shader.setFloat("power", self.power)

    class VolumetricLightShaft(Effect):
        def __init__(self):
            self.shader = Shader("misc/rendertexture/vert", "postprocessing/volumetric/lightshaft")
        
        def PassUniforms(self, shader: Shader):
            shader.setVec3("LightPos", glm.vec3(100, 100, 100).to_list())
            gl.glActiveTexture(gl.GL_TEXTURE15)
            gl.glBindTexture(gl.GL_TEXTURE_2D, GLOBAL.CURRENTRENDERCONTEXT.preoccpass)
            shader.setInt("occulusionMap", 15)
            pass
        
    def Copy(self) -> Component:
        c = PostProcessing()
        c.stack = self.stack
        c.renderTextureMesh = self.renderTextureMesh
        c.pingpongFboIDs = self.pingpongFboIDs
        c.pingpongTextureIDs = self.pingpongTextureIDs
        c.currPingPong = self.currPingPong
        return c
        
    def __init__(self):
        Component.__init__(self)
        self.stack: List[PostProcessing.Effect] = []
        self.renderTextureMesh: Mesh = None
        self.pingpongFboIDs = [None, None]
        self.pingpongTextureIDs = [None, None]
        self.currPingPong = 0
        
    def Awake(self):
        pass

    def Update(self):
        pass
    
    def AddPostProcessingEffect(self, effect: PostProcessing.Effect):
        self.stack.append(effect)
        
    def GenEffectBuffer(self):
        FBO = gl.glGenFramebuffers(1)

        # Create a 2D texture that we'll use as the framebuffer's depth buffer
        tex = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, GLOBAL.WINDOW_DIMENSIONS[0], GLOBAL.WINDOW_DIMENSIONS[1], 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR )
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
          
        # Attach it as the framebuffer's depth buffer:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, FBO)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, tex, 0)
        
        # Create renderBuffer object
        RBO = gl.glGenRenderbuffers(1)
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, RBO)
        gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH24_STENCIL8, GLOBAL.WINDOW_DIMENSIONS[0], GLOBAL.WINDOW_DIMENSIONS[1])
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, 0)
        gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_STENCIL_ATTACHMENT, gl.GL_RENDERBUFFER, RBO)
        
        # Check if framebuffer is completed with errors
        if(gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE):
            print("SUCCESS")
        
        # Unbind framebuffer and texture
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        return FBO, tex
    
    # Run by runtime
    def InitialiseEffects(self, scene: Scene):
        # Create a quad
        renderTexObj = Object("renderTexture")
        renderTexObjInst = scene.Instantiate(renderTexObj) 
        renderTex = PRIMITIVE.QUAD()
        #renderTex.mesh[0].SetMaterial(Material(effect.shader))
        renderTex.meshes[0].SetCullMode(Mesh.CULLMODE.NONE)
        renderTex.meshes[0].castShadows = False
        renderTex.meshes[0].renderPass = False
        renderTexObjInst.AddComponent(renderTex)
        
        
        #Create render textrue and framebuffer
        FBO, tex = self.GenEffectBuffer()
        FBO2, tex2 = self.GenEffectBuffer()
        
        self.pingpongFboIDs = [FBO, FBO2]
        self.pingpongTextureIDs = [tex, tex2]
        
        self.renderTextureMesh = renderTex.meshes[0]
    
    def useFBO(self):
        fboID = self.pingpongFboIDs[self.currPingPong]
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, fboID)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        
    def useTexture(self):
        textureID = self.pingpongTextureIDs[self.currPingPong]
        gl.glBindTexture(gl.GL_TEXTURE_2D, textureID)
        
    def freeFBO(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
    
    def GetTextureID(self):
        return self.pingpongTextureIDs[self.currPingPong]
    
    def PingPong(self):
        # ping pong FBOs
        self.currPingPong = 1 - self.currPingPong
        
    def RenderQuad(self, textureID: int, effect: PostProcessing.Effect):
        # Render with texture and effect
        self.renderTextureMesh.LightweightRender(effect.shader, InternalTexture(textureID), effect.PassUniforms)
    