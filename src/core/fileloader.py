from core.util import GetRootPathDir
from core.components.mesh import Mesh
import assimp_py 
import numpy as np
from core.collections.mesh import MeshCollection
from core.material import Material
from core.shader import Shader
from core.texture import Texture
import os

 # If file type isnt specified, it will try to load the file with the following extensions in order
def ValidatePath(dir:str, path:str):
    fileExtensions = [".obj",".fbx", ".blend",".3DS"]
    # Check if the path is a valid file
    if not os.path.isfile(path):
        # Check try different path exntensions
        for ext in fileExtensions:
            if not path.endswith(ext):
                # Check if file exists
                if os.path.exists(f'{dir}{path}{ext}'):
                    path += ext
                    break
            else:
                break
    return path

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
    def Load(self, modelRootName, modelRootPath = "resources/") -> MeshCollection:
        path = f'{GetRootPathDir()}/{modelRootPath}{modelRootName}'
        
        modelpath = ValidatePath(f'{path}/source/', 'model')
        
        scene = assimp_py.ImportFile(f'{path}/source/{modelpath}', self.process_flags)
        
        return  MeshLoader.GetMeshCollection(scene, modelRootName,
            albedoTexture=Texture(f"{modelRootName}/textures/albedo"),
            metallicTexture=Texture(f"{modelRootName}/textures/metallic"),
            normalTexture=Texture(f"{modelRootName}/textures/normal"),
            roughnessTexture=Texture(f"{modelRootName}/textures/roughness"),
            aoTexture=Texture(f"{modelRootName}/textures/ao"),
            emissiveTexture=Texture(f"{modelRootName}/textures/emissive"),
            )
    
    @classmethod
    def GetMeshCollection(
            self, 
            scene, 
            modelRootName,
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
            #print(mat)
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
                path = diffuse_tex[0]
                albedoTexture = Texture(f"{modelRootName}/textures/{path}")
              
            mesh = Mesh(1,vertices=verts, triangles=indices,uvs=texcoords, normals=normals)
            mesh.SetCullMode(Mesh.CULLMODE.BACK)
            mesh.SetMaterial(Material(Shader("vertex", "fragment"), diffuseTex = albedoTexture, specularTex = metallicTexture))
            meshes.addMesh(mesh)
        
        return meshes
        
