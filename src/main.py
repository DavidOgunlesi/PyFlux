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
from core.texture import Texture
from core.components.camera import Camera
from core.primitives import PRIMITIVE
import glm
from core.components.light import DirectionalLight, PointLight,SpotLight
FLOAT_SIZE = 4

def ConstructScene():
    scene = Scene()
    
    camObj = Object()
    cam = Camera()
    camObj.AddComponent(cam)
    camObjInst = scene.Instantiate(camObj)
    
    scene.SetMainCamera(camObjInst.FindComponentOfType(Camera))
    
    light = Object()
    l = scene.Instantiate(light)
    
    lightmesh = PRIMITIVE.CUBE()
    lightmesh.SetMaterial(Material(Shader("vertex", "unlit"), Texture("textures/cat.png"),  Texture("textures/cat.png")))
    
    l.transform.position = glm.vec3(3,3,3)
    l.AddComponent(lightmesh)
    l.AddComponent(DirectionalLight())
    l.AddComponent(PointLight())
    d: DirectionalLight = l.FindComponentOfType(DirectionalLight)
    d.direction = glm.vec3(-0.2, -1.0, -0.3)
    scene.SetMainLight(l)
    
    light = Object()
    l = scene.Instantiate(light)
    l.transform.position = glm.vec3(3,3,3)
    l.AddComponent(SpotLight())
    s: SpotLight = l.FindComponentOfType(SpotLight)
    s.direction = glm.vec3(0, 1, 0)
    
    testObj = Object()
    mesh = PRIMITIVE.CUBE()
    mesh.SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = Texture("textures/container2.png"), specularTex=Texture("textures/container2_specular.png")))
    testObj.AddComponent(mesh)
    scene.Instantiate(testObj)
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(10,1,0)
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(3,7,2)
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(0,4,1)
    #obj = scene.Instantiate(testObj)
    #obj.transform.position = glm.vec3(1,0,0)
    
    
    return scene

def main():
    
    # Set the caption of the screen
    pg.display.set_caption('My Window')
    
    window_size = [800, 600]
    
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
    
    # tell opengl that it should expect vertex arrays
    gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
    
    # Passes if the fragment's depth value is less than the stored depth value.
    gl.glDepthFunc(gl.GL_LESS)
    
    #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    
    runtime:Runtime = Runtime()
    
    scene = ConstructScene()
    
    runtime.SetScene(scene)
    runtime.InitRuntime()
    runtime.Run()

if __name__ == "__main__":
    main()