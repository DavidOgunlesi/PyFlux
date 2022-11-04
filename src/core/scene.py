from typing import List
from core.object import Object
import copy 
class Scene:
    def __init__(self):
        self.__objects: List[Object] = []
        
    def Instantiate(self, obj: Object) -> Object:
        obj = copy.deepcopy(obj)
        obj.Initialise(self)
        self.__objects.append(obj)
        return obj
        
    def GetObjectCollection(self):
        return self.__objects
    
    def StartScene(self):
        for obj in self.__objects:
            obj.InitialiseComponents()
            
    def UpdateScene(self):
        for obj in self.__objects:
            obj.UpdateComponents()
    