import glm
import OpenGL.GL as gl
import pygame as pg
from pygame.locals import *

import core.globals as GLOBAL
from core.components.audio import AudioClip, AudioSource
from core.components.boid import DynamicBoidManager
from core.components.camera import Camera
from core.components.light import DirectionalLight, PointLight, SpotLight
from core.components.modelRenderer import ModelRenderer
from core.components.postprocessing import PostProcessing
from core.components.terrain import TerrainMesh
from core.fileloader import MeshLoader
from core.material import Material
from core.object import Object
from core.primitives import PRIMITIVE
from core.runtime import Renderer
from core.scene import Scene
from core.shader import Shader
from core.texture import Texture

renderer:Renderer = Renderer()


def ConstructScene() -> Scene:
    '''
    # Construct Scene #
    This function is used to construct the scene
    
    Returns:
        Scene: The scene to be rendered
    '''
    scene = Scene()
    
    camObj = Object("Camera")
    cam = Camera()
    camObj.AddComponent(cam)
    camObjInst = scene.Instantiate(camObj)
    
    scene.SetMainCamera(camObjInst.FindComponentOfType(Camera))
    
    scene.SetSkyBox("textures/cubemaps/sky1")
    
    light = Object("light")
    l = scene.Instantiate(light)

    
    l.transform.position = glm.vec3(10,10,0)
    l.AddComponent(DirectionalLight())
    l.AddComponent(PointLight())
    l.transform.rotation = glm.vec3(24,23,1)
    d: DirectionalLight = l.FindComponentOfType(DirectionalLight)
    d.direction = glm.vec3(-0.2, -1.0, -0.3)
    scene.SetMainLight(l)
    
    
    light = Object("light")
    l = scene.Instantiate(light)
    l.transform.position = glm.vec3(3,3,3)
    l.AddComponent(SpotLight())
    s: SpotLight = l.FindComponentOfType(SpotLight)
    s.direction = glm.vec3(0, -1, 0)
    
    
    testObj = Object("cube")
    meshRenderer = PRIMITIVE.CUBE()
    testObj.AddComponent(meshRenderer)
    meshRenderer.meshes[0].SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = Texture("textures/blending_transparent_window.png"), specularTex=Texture("textures/blending_transparent_window.png")))
    meshRenderer.meshes[0].IgnoreCameraDistance(False)
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(10,1,0)
    o.transform.rotation = glm.vec3(24,23,1)
    
    testObj = Object("cube2")
    testObj.AddComponent(meshRenderer)
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(3,7,2)
    o =scene.Instantiate(testObj)
    o.transform.position = glm.vec3(0,4,1)
    
    modelRenderer: ModelRenderer = o.FindComponentOfType(ModelRenderer)
    
    testObj = Object("cube3")
    meshRenderer = PRIMITIVE.CUBE()
    meshRenderer.meshes[0].SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = Texture("textures/container2.png"), specularTex=Texture("textures/container2_specular.png")))
    meshRenderer.meshes[0].IgnoreCameraDistance(False)
    testObj.AddComponent(meshRenderer)


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
    '''
    # Main function #
    Initializes the engine and creates a scene
    '''
    pg.init()
    # Set the caption of the screen
    pg.display.set_caption('My Window')
    GLOBAL.WINDOW_DIMENSIONS = (1920, 1080)
    window_size = [GLOBAL.WINDOW_DIMENSIONS[0], GLOBAL.WINDOW_DIMENSIONS[1]]
    
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

if __name__ == "__main__":
    main()