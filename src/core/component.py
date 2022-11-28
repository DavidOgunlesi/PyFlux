from __future__ import annotations
from typing import TYPE_CHECKING, Type, List

if TYPE_CHECKING:
    from scene import Scene
    from core.object import Object
    from components.transform import Transform
class Component:
    
    def __init__(self):
        self.scene: Scene = None
        self.parent: Object = None
        self.transform: Transform = None
        self.name = ""
    
    def Init(self, parent: Object, scene: Scene, transform: Transform):
        self.name = parent.name
        self.scene = scene
        self.parent = parent
        self.transform = transform
        
    def GetComponent(self, type: Type) -> Component:
        return self.parent.FindComponentOfType(type)
    
    def AddComponent(self, component: Component) -> Component:
        return self.parent.AddComponent(component)
    
    def Awake(self):
        pass
    
    def Start(self):
        pass
    
    def Update(self):
        pass