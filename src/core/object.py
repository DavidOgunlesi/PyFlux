from __future__ import annotations
from typing import TYPE_CHECKING, List, Type
from core.component import Component
from core.components.transform import Transform
if TYPE_CHECKING:
    from scene import Scene

class Object:
    def __init__(self, name):
        self.components:List[Component] = []
        self.transform = Transform()
        self.components.append(self.transform)
        self.scene = None
        self.name = name
    
    def Initialise(self, scene: Scene):
        self.scene = scene
        for component in self.components:
            component.Init(parent = self, scene = self.scene, transform = self.transform)
            
    def SetupComponents(self):
        for component in self.components:
            #print("Setting up component: " + str(type(component)))
            component.Awake()
    
    def InitialiseComponents(self):
        for component in self.components:
            component.Start()
    
    def UpdateComponents(self):
        for component in self.components:
            component.Update()
            
    def AddComponent(self, component: Component):
        self.components.append(component)
        component.Init(parent = self, scene = self.scene, transform = self.transform)
        if self.scene != None and self.scene.initialised:
            component.Awake()
            component.Start()
        
    def FindComponentOfType(self, _type: Type) -> Component:
        for component in self.components:
            if type(component) is _type:
                return component
        return None