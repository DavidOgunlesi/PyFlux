from __future__ import annotations
from typing import List, TYPE_CHECKING

from core.collections.mesh import MeshCollection
from core.component import Component
from core.components.mesh import Mesh
from core.shader import Shader
import numpy as np
import glm

if TYPE_CHECKING:
    from scene import Scene
    from core.object import Object
    from components.transform import Transform
class ModelRenderer(Component):
    def Copy(self) -> Component:

        c = ModelRenderer(MeshCollection())

        for mesh in self.meshCollection.meshes:
            c.meshCollection.addMesh(mesh.Copy())
    
        c.modelMatrices = self.modelMatrices
        return c

    def __init__(self, meshes: MeshCollection):
        Component.__init__(self)
        self.meshCollection: MeshCollection = meshes
        self.modelMatrices: List[glm.mat4] = []
       
    def Init(self, parent: Object, scene: Scene, transform: Transform):
        for mesh in self.meshCollection.meshes:
            mesh.Init(self, scene, transform)
        return super().Init(parent, scene, transform)   
        
    def Awake(self):
        for mesh in self.meshCollection.meshes:
            mesh.Awake()
            mesh.modelMatrices = self.modelMatrices
            mesh.transform = self.transform
        self.NormalizeMeshCentre()
        
    def Start(self):
        for mesh in self.meshCollection.meshes:
            mesh.Start()
            mesh.transform = self.transform
        self.NormalizeMeshCentre()
            
    def Update(self):
        for mesh in self.meshCollection.meshes:
            mesh.Update()
    
    def SetShader(self, shader:Shader):
        for mesh in self.meshCollection.meshes:
            mesh.SetShader(shader)

    @property
    def materials(self):
        return list(self.__getmaterials())

    def __getmaterials(self):
        for mesh in self.meshCollection.meshes:
            yield mesh.material

    @property
    def meshes(self):
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