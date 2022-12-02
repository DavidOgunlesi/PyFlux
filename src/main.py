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
from core.components.light import DirectionalLight, PointLight,SpotLight
from core.fileloader import MeshLoader
from core.components.modelRenderer import ModelRenderer
from core.components.postprocessing import PostProcessing
from core.component import Component
from core.components.terrain import TerrainMesh
import math
from core.components.boid import DynamicBoidManager
from core.components.audio import AudioSource, AudioClip
renderer:Runtime = Runtime()

def GetPoseMatrices(i: int, c:Component, size: int):
    # Create vectors in a grid based on i index, with spacing
    spacing = 3
    vec = glm.vec3(((i+1) % math.sqrt(size)) * spacing, 0, ( math.floor(i / math.sqrt(size))) * spacing)
    poseMtx = c.transform.GetPoseMatrix(translation=vec)
    mat4Arr = np.array(poseMtx, dtype=np.float32)
    mat4Arr = mat4Arr.flatten()
    return mat4Arr

def ConstructScene():
    scene = Scene()
    
    
    camObj = Object("Camera")
    cam = Camera()
    camObj.AddComponent(cam)
    camObjInst = scene.Instantiate(camObj)
    
    scene.SetMainCamera(camObjInst.FindComponentOfType(Camera))
    
    scene.SetSkyBox("textures/cubemaps/sky1")
    
    light = Object("light")
    l = scene.Instantiate(light)

    #meshRenderer = PRIMITIVE.CUBE()
    #meshRenderer.mesh[0].SetMaterial(Material(Shader("vertex", "unlit"), Texture("textures/cat.png"),  Texture("textures/cat.png")))
    
    l.transform.position = glm.vec3(10,10,0)
    #l.AddComponent(meshRenderer)
    l.AddComponent(DirectionalLight())
    l.AddComponent(PointLight())
    l.transform.rotation = glm.vec3(24,23,1)
    d: DirectionalLight = l.FindComponentOfType(DirectionalLight)
    d.direction = glm.vec3(-0.2, -1.0, -0.3)
    scene.SetMainLight(l)
    
    # # render tex
    # ro = Object("render tex")
    # renderTex = PRIMITIVE.QUAD()
    # renderTex.mesh[0].SetMaterial(Material(Shader("misc/rendertexture/vert", "misc/rendertexture/frag")))
    # renderTex.mesh[0].SetCullMode(Mesh.CULLMODE.NONE)
    # renderTex.mesh[0].castShadows = False
    # renderTex.mesh[0].renderPass = False
    # ro.AddComponent(renderTex)
    
    # o = scene.Instantiate(ro)
    # renderer.renderTexMesh = o.FindComponentOfType(ModelRenderer).mesh[0]
    
    light = Object("light")
    l = scene.Instantiate(light)
    l.transform.position = glm.vec3(3,3,3)
    l.AddComponent(SpotLight())
    s: SpotLight = l.FindComponentOfType(SpotLight)
    s.direction = glm.vec3(0, -1, 0)
    
    # sprPb = Object()
    # spr = scene.Instantiate(sprPb)
    # spr.transform.position = glm.vec3(-3,-3,-3)
    # spr.AddComponent(SpriteRenderer(Texture("textures/light.png")))
    
    testObj = Object("cube")
    meshRenderer = PRIMITIVE.CUBE()
    testObj.AddComponent(meshRenderer)
    meshRenderer.meshes[0].SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = Texture("textures/blending_transparent_window.png"), specularTex=Texture("textures/blending_transparent_window.png")))
    meshRenderer.meshes[0].IgnoreCameraDistance(False)
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(10,1,0)
    o.transform.rotation = glm.vec3(24,23,1)
    
    testObj = Object("cube2")
    #meshRenderer = PRIMITIVE.CUBE()
    #meshRenderer.mesh[0].SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = Texture("textures/container2.png"), specularTex=Texture("textures/container2_specular.png")))
    testObj.AddComponent(meshRenderer)
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(3,7,2)
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(0,4,1)
    
    modelRenderer: ModelRenderer = o.FindComponentOfType(ModelRenderer)
    
    # size = 200*200
    # modelRenderer.modelMatrices = np.array([GetPoseMatrices(i, modelRenderer.meshes[0], size) for i in range(size)])

    testObj = Object("cube3")
    meshRenderer = PRIMITIVE.CUBE()
    meshRenderer.meshes[0].SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = Texture("textures/container2.png"), specularTex=Texture("textures/container2_specular.png")))
    meshRenderer.meshes[0].IgnoreCameraDistance(False)
    testObj.AddComponent(meshRenderer)

    # for i in range(0, 50):
    #     birdBoid = Object("bird boid"); 
    #     birdBoid.AddComponent(Boid())
    #     scene.Instantiate(birdBoid)

    birdBoid = Object("bird boid Manger"); 
    birdBoid.AddComponent(DynamicBoidManager())
    scene.Instantiate(birdBoid)

    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(10,1,0)
    o.transform.rotation = glm.vec3(24,23,1)

    obj = scene.Instantiate(testObj)
    obj.transform.position = glm.vec3(1,0,0)
    
    shipwreckObjPrefab = Object("shipwreck")
    modelRenderer = ModelRenderer(MeshLoader.Load("models/shipwreck"))
    #modelRenderer = ModelRenderer(MeshLoader.Load("suzanne.obj"))
    shipwreckObjPrefab.AddComponent(modelRenderer)
    shipwreckObj = scene.Instantiate(shipwreckObjPrefab)
    shipwreckObj.transform.position = glm.vec3(0,-900, 3400)
    shipwreckObj.transform.scale = glm.vec3(2,2,2)
    shipwreckObj.transform.rotation = glm.vec3(0,90,0)

    
    planeObj = Object("plane")
    meshRenderer = PRIMITIVE.PLANE()
    meshRenderer.meshes[0].SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = None, specularTex=None))
    planeObj.AddComponent(meshRenderer)
    o = scene.Instantiate(planeObj)
    
    o.transform.position = glm.vec3(0,-1,0)
    o.transform.scale = glm.vec3(21,20,20)
    
    terrainObj = Object("terrain")
    terrainObj.AddComponent(TerrainMesh(90))
    scene.Instantiate(terrainObj)
    
    soundObject = Object("sougnd")
    audioSource = AudioSource(AudioClip("sounds/river-surroundings"), 0)
    audioSource.playOnAwake = True
    soundObject.AddComponent(audioSource)
    audioSource.SetVolume(1)
    audioSource.SetAttenution(90*2,600)

    audioSource = AudioSource(AudioClip("sounds/river-and-birds"), 1)
    audioSource.playOnAwake = True
    soundObject.AddComponent(audioSource)
    audioSource.SetVolume(0.3)
    audioSource.SetAttenution(140*2,600)

    audioSource = AudioSource(AudioClip("sounds/river-surroundings"), 2)
    audioSource.playOnAwake = True
    soundObject.AddComponent(audioSource)
    audioSource.SetVolume(0.2)
    audioSource.SetAttenution(40*2,600)

    audioSource = AudioSource(AudioClip("sounds/jungle_ambience"), 3)
    audioSource.playOnAwake = True
    soundObject.AddComponent(audioSource)
    audioSource.SetVolume(0.2)
    audioSource.SetAttenution(20*6,600)

    audioSource = AudioSource(AudioClip("sounds/light-wind"), 4)
    audioSource.playOnAwake = True
    soundObject.AddComponent(audioSource)
    audioSource.SetVolume(0.2)
    audioSource.SetAttenution(2000,-900)

    scene.Instantiate(soundObject)
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
    #gl.glPolygonMode(gl.GL_FRONT, gl.GL_LINE)
    #gl.glPolygonMode(gl.GL_BACK, gl.GL_LINE)
    # tell opengl that it should expect vertex arrays
    gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
    
    # Passes if the fragment's depth value is less than the stored depth value.
    gl.glDepthFunc(gl.GL_LESS)
    
    #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

    
    scene = ConstructScene()
    
    renderer.SetScene(scene)
    
    postProcessing = PostProcessing()
    #postProcessing.AddPostProcessingEffect(PostProcessing.Inversion())
    renderer.AddPostProcessing(postProcessing)
    
    renderer.InitRuntime()
    renderer.Run()


# def pygame_event_loop(loop, event_queue):
#     while True:
#         event = pg.event.wait()
#         asyncio.run_coroutine_threadsafe(event_queue.put(event), loop=loop)

# async def mainloop():
#     current_time = 0
#     while True:
#         last_time, current_time = current_time, time.time()
#         print(1/(current_time-last_time))
        
#         await asyncio.sleep(1 / 60 - (current_time - last_time))  # tick

# async def sideloop():
#     current_time = 0
#     while True:
#         last_time, current_time = current_time, time.time()
        
#         await asyncio.sleep(1 / 60 - (current_time - last_time))  # tick       

# def loop():
#     loop = asyncio.get_event_loop()
#     event_queue = asyncio.Queue()

#     pygame_task = loop.run_in_executor(None, pygame_event_loop, loop, event_queue)
#     main_loop = asyncio.ensure_future(mainloop())
#     side_loop = asyncio.ensure_future(sideloop())
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         pygame_task.cancel()
#         main_loop.cancel()
#         side_loop.cancel()

#     pg.quit()

if __name__ == "__main__":
    main()