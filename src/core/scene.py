from typing import List
from core.object import Object
import copy 
from core.components.camera import Camera
class Scene:
    def __init__(self):
        self.__objects: List[Object] = []
        self.mainCamera = None
        
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
            obj.InitialiseComponents()
            
    def UpdateScene(self):
        if self.mainCamera == None:
            print("Main Camera not set, scene disabled")
            return
        for obj in self.__objects:
            obj.UpdateComponents()
    
    def SetMainCamera(self, camera:Camera):
        self.mainCamera = camera