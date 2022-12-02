from typing import List, Callable
from core.object import Object
import copy 
from core.components.camera import Camera
from core.collections.light import LightCollection
from core.components.light import Light, DirectionalLight
from core.components.skybox import Skybox
from core.components.mesh import Mesh
from core.components.modelRenderer import ModelRenderer
from core.component import Component
import time
import threading
import pygame as pg
class Scene:
    
    def __init__(self):
        self.initialised = False
        self.__objects: List[Object] = []
        self.mainCamera:Camera = None
        self.mainLight: DirectionalLight = None
        self.lightCollection = LightCollection()
        self.skybox: Skybox = None
        self.__componentsToSetup: List[Component] = []
        
    def Instantiate(self, obj: Object) -> Object:
        return self.InstantiateOnThread(obj, None)

    def InstantiateThreaded(self, obj: Object, callback:Callable = None) -> Object:
        start = time.time()
        x = threading.Thread(target=self.InstantiateOnThread, args=(obj,callback))
        x.start()
        #print("Instantiate time: ", time.time() - start)

    def InstantiateOnThread(self, obj: Object, callback:Callable):
        pg.event.pump()
        obj2 = obj.Copy()
        obj2.Initialise(self)
        self.__objects.append(obj2)
        for component in obj2.components:
            self.QueueComponentSetup(component)

        if callback != None:
            callback(obj2)
            
        return obj2


    def GetObjectCollection(self):
        return self.__objects
    
    def StartScene(self):
        if self.mainCamera == None:
            print("Main Camera not set, scene disabled")
            return
        for obj in self.__objects:
            print("Awaking object", obj.name)
            obj.SetupComponents()
        for obj in self.__objects:
            if not obj.awake:
                continue
            print("Starting object", obj.name)
            obj.InitialiseComponents()
        print("/////////////////////////////////Scene started////////////////////////////////")
        self.initialised = True
            
    def UpdateScene(self):
        if self.mainCamera == None:
            print("Main Camera not set, scene disabled")
            return
        for component in self.__componentsToSetup:
            if not component.parent.awake:
                component.Awake()
            if not component.parent.started:
                component.Start()
        self.__componentsToSetup.clear()

        for obj in self.__objects:
            obj.UpdateComponents()

        for obj in self.__objects:
            obj.LateUpdateComponents()
        
    
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

    def RemoveObject(self, obj: Object):
        self.__objects.remove(obj)

    def QueueComponentSetup(self, component):
        self.__componentsToSetup.append(component)