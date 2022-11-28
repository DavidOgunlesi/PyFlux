from __future__ import annotations
from typing import List, TYPE_CHECKING

from core.collections.mesh import MeshCollection
from core.component import Component
from core.components.mesh import Mesh
import numpy as np
import glm

if TYPE_CHECKING:
    from scene import Scene
    from core.object import Object
    from components.transform import Transform
class ModelRenderer(Component):
    def __init__(self, meshes: MeshCollection):
        Component.__init__(self)
        self.meshCollection: MeshCollection = meshes
       
    def Init(self, parent: Object, scene: Scene, transform: Transform):
        for mesh in self.meshCollection.meshes:
            mesh.Init(self, scene, transform)
        return super().Init(parent, scene, transform)   
        
    def Awake(self):
        for mesh in self.meshCollection.meshes:
            mesh.Awake()
        self.NormalizeMeshCentre()
        
    def Start(self):
        for mesh in self.meshCollection.meshes:
            mesh.Start()
        self.NormalizeMeshCentre()
            
    def Update(self):
        for mesh in self.meshCollection.meshes:
            mesh.Update()
    
    @property
    def mesh(self):
        return self.meshCollection.meshes
    
    def NormalizeMeshCentre(self):
        # Get the centre of the mesh (in world space)
        avgCentre = glm.vec3(0,0,0)
        for mesh in self.meshCollection.meshes:
            centre = mesh.GetMeshCentre()
            
            # Convert to world space
            
            avgCentre.x += centre[0]
            avgCentre.y += centre[1]
            avgCentre.z += centre[2]
            
        avgCentre /= self.meshCollection.size
        
        for mesh in self.meshCollection.meshes:
            # offset mesh by average centre to centre mesh in local space
            mesh.offset = -avgCentre