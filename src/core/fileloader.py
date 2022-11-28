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
    def Load(self, modelRootName, modelRootPath = "resources/models/") -> MeshCollection:
        path = f'{GetRootPathDir()}/{modelRootPath}{modelRootName}'
        modelpath = f'{path}/source/model.obj'
        scene = assimp_py.ImportFile(modelpath, self.process_flags)
        
        return  MeshLoader.GetMeshCollection(scene, 
            albedoTexture=Texture(f"models/{modelRootName}/textures/albedo"),
            metallicTexture=Texture(f"models/{modelRootName}/textures/metallic"),
            normalTexture=Texture(f"models/{modelRootName}/textures/normal"),
            roughnessTexture=Texture(f"models/{modelRootName}/textures/roughness"),
            aoTexture=Texture(f"models/{modelRootName}/textures/ao"),
            emissiveTexture=Texture(f"models/{modelRootName}/textures/emissive"),
            )
    
    @classmethod
    def GetMeshCollection(
            self, 
            scene, 
            albedoTexture:Texture = None, 
            normalTexture:Texture = None, 
            metallicTexture:Texture = None, 
            roughnessTexture:Texture = None, 
            aoTexture:Texture = None, 
            emissiveTexture:Texture = None
            ):
        
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
            """
            Material Format:
            {
                'NAME': 'DefaultMaterial', 
                'SHADING_MODEL': 2, 
                'COLOR_AMBIENT': [0.0, 0.0, 0.0], 
                'COLOR_DIFFUSE': [0.6000000238418579, 0.6000000238418579, 0.6000000238418579], 
                'COLOR_SPECULAR': [0.0, 0.0, 0.0], 
                'COLOR_EMISSIVE': [0.0, 0.0, 0.0], 
                'SHININESS': 0.0, 
                'OPACITY': 1.0, 
                'COLOR_TRANSPARENT': [1.0, 1.0, 1.0], 
                'REFRACTI': 1.0, 
                'TEXTURES': {}
            }
            """
            # -- getting textures
            if mat["TEXTURES"]:
                diffuse_tex = mat["TEXTURES"][assimp_py.TextureType_DIFFUSE]
                   
            mesh = Mesh(1,vertices=verts, triangles=indices,uvs=texcoords, normals=normals)
            mesh.SetCullMode(Mesh.CULLMODE.BACK)
            mesh.SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = albedoTexture, specularTex = metallicTexture))
            meshes.addMesh(mesh)
        
        return meshes
        
