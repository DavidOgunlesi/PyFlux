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
FLOAT_SIZE = 4

def ConstructScene():
    scene = Scene()
    
    camObj = Object()
    cam = Camera()
    camObj.AddComponent(cam)
    camObjInst = scene.Instantiate(camObj)
    
    scene.SetMainCamera(camObjInst.FindComponentOfType(Camera))
    
    light = Object()
    lightmesh = PRIMITIVE.CUBE()
    lightmesh.SetMaterial(Material(Shader("vertex", "unlit"), Texture("textures/cat.png")))
    light.AddComponent(lightmesh)
    o = scene.Instantiate(light)
    o.transform.position = glm.vec3(3,3,3)
    scene.SetMainLight(o)
    
    testObj = Object()
    mesh = PRIMITIVE.CUBE()
    mesh.SetMaterial(Material(Shader("vertex", "fragment"), Texture("textures/cat.png")))
    testObj.AddComponent(mesh)
    scene.Instantiate(testObj)
    
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