from typing import List
from core.object import Object
import copy 
from core.components.camera import Camera
from core.collections.light import LightCollection
from core.components.light import Light, DirectionalLight
from core.components.skybox import Skybox
from core.components.mesh import Mesh
from core.components.modelRenderer import ModelRenderer
class Scene:
    
    def __init__(self):
        self.initialised = False
        self.__objects: List[Object] = []
        self.mainCamera:Camera = None
        self.mainLight: DirectionalLight = None
        self.lightCollection = LightCollection()
        self.skybox: Skybox = None
        
    def Instantiate(self, obj: Object) -> Object:
        obj = copy.deepcopy(obj)
        obj.Initialise(self)
        self.__objects.append(obj)
        return obj
        
    def GetObjectCollection(self):
        return self.__objects
    
    def StartScene(self):
        if self.mainCamera == None:
            print("Main Camera not set, scene disabled")
            return
        for obj in self.__objects:
            obj.SetupComponents()
        for obj in self.__objects:
            obj.InitialiseComponents()
        self.initialised = True
            
    def UpdateScene(self):
        if self.mainCamera == None:
            print("Main Camera not set, scene disabled")
            return
        for obj in self.__objects:
            obj.UpdateComponents()
    
    def GetMeshes(self):
        meshes = []
        for obj in self.__objects:
            mesh = obj.FindComponentOfType(Mesh)
            if mesh != None:
                meshes.append(mesh)
            modelRenderer: ModelRenderer = obj.FindComponentOfType(ModelRenderer)
            if modelRenderer != None:
                meshes.extend(modelRenderer.meshCollection.meshes)
        return meshes
    
    def SetMainCamera(self, camera:Camera):
        self.mainCamera = camera
        
    def SetMainLight(self, obj: Object):
        light = obj.FindComponentOfType(DirectionalLight)
        if light != None:
            self.lightCollection.setGlobalLight(light)
            self.mainLight = light
            
    def SetSkyBox(self, path):
        faces = [
            "right.jpg",
            "left.jpg",
            "top.jpg",
            "bottom.jpg",
            "front.jpg",
            "back.jpg"
            ]
        skyboxObj = Object("skybox")
        sky = Skybox(path, faces)
        skyboxObj.AddComponent(sky)
        skyboxObjInst = self.Instantiate(skyboxObj)
        self.skybox = skyboxObjInst.FindComponentOfType(Skybox)