from core.collections.mesh import MeshCollection
from core.components.mesh import Mesh
from core.components.modelRenderer import ModelRenderer


class PRIMITIVE:
    '''
    PRIMITIVE is a class that contains static methods that return a mesh.
    '''
    @classmethod
    def CUBE(cls):
        # CUBE
        vertices=[
            #vPos  color  uv
            [0,0,0],
            [1,0,0],
            [0,1,0],
            [1,1,0], 
            [0,0,1], 
            [1,0,1],
            [0,1,1],
            [1,1,1],
            ]
        colors=[
            #vPos
            [1,1,1],
            [1,1,1],
            [1,1,1],
            [1,1,1], 
            [1,1,1],
            [1,1,1],
            [1,1,1],
            [1,1,1],
            ]
        uvs=[
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            ]
        triangles = [
            2,0,3,
            3,0,1,
            4,6,5,
            5,6,7,
            0,4,1,
            1,4,5,
            1,5,3,
            3,5,7,
            3,7,2,
            2,7,6,
            2,6,0,
            0,6,4
        ]
        mc = MeshCollection()
        mc.addMesh(Mesh(0, vertices=vertices, triangles=triangles, colors = colors, uvs=uvs))
        return ModelRenderer(mc)
    
    @classmethod
    def UNITCUBE(cls):
        # CUBE
        vertices=[
            #vPos  color  uv
            [-1,-1,-1],
            [1,-1,-1],
            [-1,1,-1],
            [1,1,-1], 
            [1,-1,1], 
            [1,-1,1],
            [-1,1,1],
            [1,1,1],
            ]
        colors=[
            #vPos
            [1,1,1],
            [1,1,1],
            [1,1,1],
            [1,1,1], 
            [1,1,1],
            [1,1,1],
            [1,1,1],
            [1,1,1],
            ]
        uvs=[
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            ]
        triangles = [
            2,0,3,
            3,0,1,
            4,6,5,
            5,6,7,
            0,4,1,
            1,4,5,
            1,5,3,
            3,5,7,
            3,7,2,
            2,7,6,
            2,6,0,
            0,6,4
        ]
        mc = MeshCollection()
        mc.addMesh(Mesh(0, vertices=vertices, triangles=triangles, colors = colors, uvs=uvs))
        return ModelRenderer(mc)
    
    @classmethod
    def QUAD(cls):
        vertices=[
            #vPos  color  uv
            [-1,-1,0],
            [1,-1,0],
            [-1,1,0],
            [1,1,0],
            ]
        colors=[
            #vPos
            [1,1,1],
            [1,1,1],
            [1,1,1],
            [1,1,1],
            ]
        uvs=[
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            ]
        triangles = [
            2,0,3,
            3,0,1,
        ]
        #return Mesh(0, vertices=vertices, triangles=triangles, colors = colors, uvs=uvs)
        mc = MeshCollection()
        mc.addMesh(Mesh(0, vertices=vertices, triangles=triangles, colors = colors, uvs=uvs))
        return ModelRenderer(mc)
    
    @classmethod
    def PLANE(cls):
        vertices=[
            #vPos  color  uv
            [-1,0,-1],
            [1,0,-1],
            [-1,0,1],
            [1,0,1],
            ]
        colors=[
            #vPos
            [1,1,1],
            [1,1,1],
            [1,1,1],
            [1,1,1],
            ]
        uvs=[
            [0,0],[0,1],[1,0],
            [1,0],[0,1],[1,1],
            ]
        triangles = [
            2,0,3,
            3,0,1,
        ]
        #return Mesh(0, vertices=vertices, triangles=triangles, colors = colors, uvs=uvs)
        mc = MeshCollection()
        mc.addMesh(Mesh(0, vertices=vertices, triangles=triangles, colors = colors, uvs=uvs))
        return ModelRenderer(mc)
    
    @classmethod
    def PLANE_PATCHES(cls):
        vertices=[
            #vPos  color  uv
            [-1,0,-1],
            [1,0,-1],
            [-1,0,1],
            [1,0,1],
            ]
        colors=[
            #vPos
            [1,1,1],
            [1,1,1],
            [1,1,1],
            [1,1,1],
            ]
        uvs=[
            [1,1],[1,0],[0,0],[0,1]
            ]
        triangles = [
            0,1,2,3
        ]
        normals = [
            [0,1,0],
            [0,1,0],
            [0,1,0],
            [0,1,0],
        ]
        #return Mesh(0, vertices=vertices, triangles=triangles, colors = colors, uvs=uvs)
        mc = MeshCollection()
        m = Mesh(0, vertices=vertices, triangles=triangles, colors = colors, uvs=uvs, normals=normals)
        mc.addMesh(m)
        return ModelRenderer(mc)
