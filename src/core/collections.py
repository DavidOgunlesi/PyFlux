from core.components.light import Light
from typing import List

class LightCollection:
    def __init__(self):
        self.globalLight:Light = None 
        self.lights: List[Light] = []
        
    def addLight(self, light: Light):
        self.lights.append(light)
        
    def setGlobalLight(self, light: Light):
        self.globalLight = light