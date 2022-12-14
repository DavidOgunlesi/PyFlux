from __future__ import annotations

from typing import TYPE_CHECKING, List

import glm

from core.collections.mesh import MeshCollection
from core.component import Component
from core.shader import Shader

if TYPE_CHECKING:
    from scene import Scene
    from core.object import Object
    from components.transform import Transform

import copy


class ModelRenderer(Component):
    '''
    Modelrendereer is a component that renders a collection of meshes.
    '''
    
    def Copy(self) -> Component:

        c = ModelRenderer(MeshCollection())

        for mesh in self.meshCollection.meshes:
            c.meshCollection.addMesh(mesh.Copy())
    
        c.modelMatrices = copy.deepcopy(self.modelMatrices)
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

    def LateUpdate(self):
        for mesh in self.meshCollection.meshes:
            mesh.LateUpdate()
    
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