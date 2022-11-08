from core.util import GetRootPathDir
from core.components.mesh import Mesh
import assimp_py 
import numpy as np
from core.collections.mesh import MeshCollection
from core.material import Material
from core.shader import Shader
from core.texture import Texture
class MeshLoader:
    
    process_flags = (
        assimp_py.Process_Triangulate | 
        #assimp_py.Process_CalcTangentSpace |
        assimp_py.Process_FlipUVs |
        assimp_py.Process_GenNormals |
        assimp_py.Process_OptimizeMeshes
    )
    
    def __init__(self):
        pass
    
    @classmethod
    def Load(self, fileName, modelRootPath = "resources/models/") -> MeshCollection:
        path = f'{GetRootPathDir()}/{modelRootPath}{fileName}'
        scene = assimp_py.ImportFile(path, self.process_flags)
        
        return  MeshLoader.GetMeshCollection(scene)
    
    @classmethod
    def GetMeshCollection(self, scene):
        meshes:MeshCollection = MeshCollection()
        # -- getting data
        for m in scene.meshes:
            # -- getting vertex data
            # vertices are guaranteed to exist
            verts = m.vertices
            
            verts = np.array( verts, np.float32)
            #print("verts",len(verts))
            # # other components must be checked for None
            normals = [] or m.normals
            normals = np.array( normals, np.float32)
            
            texcoords = [] or m.texcoords
            if not texcoords == []:
                texcoords = np.array( texcoords[0], np.float32)
            
            indices = [] or m.indices
            indices = np.array( indices, np.int32)
            #tangents = [] or m.tangents
            #bitangent = [] or m.bitangents

            # -- getting materials
            # mat is a dict consisting of assimp material properties
            mat = scene.materials[m.material_index]

            # -- getting color
            diffuse_color = mat["COLOR_DIFFUSE"]
            
            # -- getting textures
            if mat["TEXTURES"]:
                diffuse_tex = mat["TEXTURES"][assimp_py.TextureType_DIFFUSE]
                
            mesh = Mesh(1,vertices=verts, triangles=indices,uvs=texcoords, normals=normals)
            mesh.SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = Texture("textures/container2.png"), specularTex=Texture("textures/container2_specular.png")))
            meshes.addMesh(mesh)
        
        return meshes
        
