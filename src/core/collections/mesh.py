from core.components.mesh import Mesh
from typing import List

class MeshCollection:
    def __init__(self):
        self.meshes: List[Mesh] = []
        
    def addMesh(self, mesh: Mesh):
        self.meshes.append(mesh)
        
    @property
    def size(self):
        return len(self.meshes)