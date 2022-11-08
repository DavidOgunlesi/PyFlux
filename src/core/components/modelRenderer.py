from typing import List

from core.collections.mesh import MeshCollection
from core.component import Component
from core.components.mesh import Mesh
import numpy as np
import glm
class ModelRenderer(Component):
    def __init__(self, meshes: MeshCollection):
        self.meshCollection: MeshCollection = meshes
        
    def Start(self):
        for mesh in self.meshCollection.meshes:
            mesh.Init(self, self.scene, self.transform)
            
        self.NormalizeMeshCentre()
            
    def Update(self):
        for mesh in self.meshCollection.meshes:
            mesh.Render()
    
    @property
    def mesh(self):
        return self.meshCollection.meshes
    
    def NormalizeMeshCentre(self):
        avgCentre = glm.vec3(0,0,0)
        for mesh in self.meshCollection.meshes:
            centre = mesh.GetMeshCentre()
            avgCentre.x += centre[0]
            avgCentre.y += centre[1]
            avgCentre.z += centre[2]
            
        #print(avgCentre)
        avgCentre /= self.meshCollection.size
        
        for mesh in self.meshCollection.meshes:
            # offset mesh by average centre to centre mesh in local space
            mesh.offset = -avgCentre
            #print(mesh.offset, avgCentre)