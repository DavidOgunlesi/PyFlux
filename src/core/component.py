from __future__ import annotations
from typing import TYPE_CHECKING, Type, List
import copy
if TYPE_CHECKING:
    from scene import Scene
    from core.object import Object
    from components.transform import Transform
class Component:
    
    def __init__(self):
        self.scene: Scene = None
        self.parent: Object = None
        self.transform: Transform = None
    
    def Init(self, parent: Object, scene: Scene, transform: Transform):
        self.scene = scene
        self.parent = parent
        self.transform = transform
        
    @property
    def name(self):
        return self.parent.name

    def GetComponent(self, type: Type) -> Component:
        return self.parent.FindComponentOfType(type)
    
    def AddComponent(self, component: Component) -> Component:
        return self.parent.AddComponent(component)
    
    def Copy(self) -> Component:
        pass

    def Awake(self):
        pass
    
    def Start(self):
        pass
    
    def Update(self):
        pass

    def LateUpdate(self):
        pass

    def OnDestroy(self):
        pass