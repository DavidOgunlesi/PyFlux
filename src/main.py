import ctypes
import time

import glm
import numpy as np
import OpenGL.GL as gl
import pygame as pg
from core.components.mesh import Mesh
from core.components.transform import Transform
from core.material import Material
from core.object import Object
from pygame.locals import *
from core.runtime import Runtime
from core.scene import Scene
from core.shader import Shader
from core.texture import Texture, CubeMap
from core.components.camera import Camera
from core.components.sprite import SpriteRenderer
from core.primitives import PRIMITIVE
import glm
from core.components.light import DirectionalLight, PointLight,SpotLight
from core.fileloader import MeshLoader
from core.components.modelRenderer import ModelRenderer
runtime:Runtime = Runtime()

def ConstructScene():
    scene = Scene()
    
    
    camObj = Object()
    cam = Camera()
    camObj.AddComponent(cam)
    camObjInst = scene.Instantiate(camObj)
    
    scene.SetMainCamera(camObjInst.FindComponentOfType(Camera))
    
    #scene.SetSkyBox("textures/cubemaps/sky1")
    
    light = Object()
    l = scene.Instantiate(light)

    #meshRenderer = PRIMITIVE.CUBE()
    #meshRenderer.mesh[0].SetMaterial(Material(Shader("vertex", "unlit"), Texture("textures/cat.png"),  Texture("textures/cat.png")))
    
    l.transform.position = glm.vec3(0,0,0)
    #l.AddComponent(meshRenderer)
    l.AddComponent(DirectionalLight())
    l.AddComponent(PointLight())
    l.transform.rotation = glm.vec3(24,23,1)
    d: DirectionalLight = l.FindComponentOfType(DirectionalLight)
    d.direction = glm.vec3(-0.2, -1.0, -0.3)
    scene.SetMainLight(l)
    
    #render tex
    # ro = Object()
    # renderTex = PRIMITIVE.QUAD()
    # renderTex.mesh[0].SetMaterial(Material(Shader("misc/rendertexture/vert", "misc/rendertexture/frag")))
    # renderTex.mesh[0].SetCullMode(Mesh.CULLMODE.NONE)
    # renderTex.mesh[0].renderShadowMap = False
    # ro.AddComponent(renderTex)
    
    #o = scene.Instantiate(ro)
    #runtime.renderTexMesh = o.FindComponentOfType(ModelRenderer).mesh[0]
    
    light = Object()
    l = scene.Instantiate(light)
    l.transform.position = glm.vec3(3,3,3)
    l.AddComponent(SpotLight())
    s: SpotLight = l.FindComponentOfType(SpotLight)
    s.direction = glm.vec3(0, 1, 0)
    
    # sprPb = Object()
    # spr = scene.Instantiate(sprPb)
    # spr.transform.position = glm.vec3(-3,-3,-3)
    # spr.AddComponent(SpriteRenderer(Texture("textures/light.png")))
    
    testObj = Object()
    meshRenderer = PRIMITIVE.CUBE()
    meshRenderer.mesh[0].SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = Texture("textures/blending_transparent_window.png"), specularTex=Texture("textures/blending_transparent_window.png")))
    meshRenderer.mesh[0].IgnoreCameraDistance(False)
    testObj.AddComponent(meshRenderer)
    
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(10,1,0)
    o.transform.rotation = glm.vec3(24,23,1)
    
    testObj = Object()
    #meshRenderer = PRIMITIVE.CUBE()
    #meshRenderer.mesh[0].SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = Texture("textures/container2.png"), specularTex=Texture("textures/container2_specular.png")))
    testObj.AddComponent(meshRenderer)
    
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(3,7,2)
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(0,4,1)
    obj = scene.Instantiate(testObj)
    obj.transform.position = glm.vec3(1,0,0)
    
    bagObjPrefab = Object()
    #modelRenderer = ModelRenderer(MeshLoader.Load("bag\source\Survival_BackPack_2.obj"))
    modelRenderer = ModelRenderer(MeshLoader.Load("suzanne.obj"))
    bagObjPrefab.AddComponent(modelRenderer)
    bagObj = scene.Instantiate(bagObjPrefab)
    bagObj.transform.position = glm.vec3(-5,-5,0)
    bagObj.transform.scale = glm.vec3(1,1,1)
    bagObj.transform.rotation = glm.vec3(24,23,1)
    
    planeObj = Object()
    meshRenderer = PRIMITIVE.PLANE()
    meshRenderer.mesh[0].SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = None, specularTex=None))
    planeObj.AddComponent(meshRenderer)
    o = scene.Instantiate(planeObj)
    o.transform.position = glm.vec3(0,-1,0)
    o.transform.scale = glm.vec3(21,20,20)
    
    return scene

def main():
    pg.init()
    # Set the caption of the screen
    pg.display.set_caption('My Window')
    
    window_size = [800, 600]
    
    pg.display.gl_set_attribute(GL_STENCIL_SIZE, 8)
    # Enable double frame buffering and tell pygame to use opengl context
    pg.display.set_mode([window_size[0], window_size[1]], DOUBLEBUF|OPENGL)
    
    pg.mouse.set_visible(False)
    pg.event.set_grab(True)
    # tell opengl we need a renderering viewport of 800 by 600
    # open gl beind the scenes maps normalised vieewport points i.e. 0 to 1 to pixel coords i.e. 304px to 783px
    # we are telling it to map 0 to 1 to 0 to 800 and 0 to 600 in x and y respectively
    gl.glViewport(0, 0, window_size[0], window_size[1])
    
    # Set background colour for opengl
    gl.glClearColor(0, 0, 0, 1)
    
     # Enable depth test to let opengl store depth buffer
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_STENCIL_TEST)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    
    gl.glFrontFace(gl.GL_CCW)
    
    gl.glEnable(gl.GL_FRAMEBUFFER_SRGB)
    
    # tell opengl that it should expect vertex arrays
    gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
    
    # Passes if the fragment's depth value is less than the stored depth value.
    gl.glDepthFunc(gl.GL_LESS)
    
    #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

    
    scene = ConstructScene()
    
    runtime.SetScene(scene)
    runtime.InitRuntime()
    runtime.Run()

if __name__ == "__main__":
    main()