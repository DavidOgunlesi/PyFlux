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
        self.awake = False
        self.started = False
    
    def Initialise(self, scene: Scene):
        self.scene = scene
        for component in self.components:
            component.Init(parent = self, scene = self.scene, transform = self.transform)
            
    def SetupComponents(self):
        self.awake = True
        for component in self.components:
            component.Awake()
    
    def InitialiseComponents(self):
        self.started = True
        for component in self.components:
            component.Start()
    
    def UpdateComponents(self):
        for component in self.components:
            component.Update()

    def LateUpdateComponents(self):
        for component in self.components:
            component.LateUpdate()

    def AddComponent(self, component: Component):
        self.components.append(component)
        component.Init(parent = self, scene = self.scene, transform = self.transform)
        if self.scene != None and self.scene.initialised:
            self.scene.QueueComponentSetup(component)
        
    def FindComponentOfType(self, _type: Type) -> Component:
        for component in self.components:
            if type(component) is _type:
                return component
        return None

    def Destroy(self):
        self.scene.RemoveObject(self)
        for component in self.components:
            component.OnDestroy()
        for component in self.components:
            del component
        self.components.clear()
        self.scene = None
        self.transform = None

    def Copy(self):
        newObj = Object(self.name)
        newObj.components.clear()
        
        for component in self.components:
            newObj.components.append(component.Copy())
        #print("Copied object: ", self.components , newObj.components)
        newObj.transform = self.transform.Copy()
        newObj.name = self.name
        return newObj