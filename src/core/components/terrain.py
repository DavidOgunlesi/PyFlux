from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, List, Dict, Any
from core.texture import GeneratedTexture, Texture
from core.component import Component
from core.components.mesh import Mesh
from core.primitives import PRIMITIVE
from core.shader import Shader
from core.object import Object
from core.material import Material
import OpenGL.GL as gl
import glm
import core.gametime as gametime
import core.globals as GLOBAL
import pygame as pg
from perlin_noise import PerlinNoise
from core.collections.mesh import MeshCollection
from core.components.modelRenderer import ModelRenderer

if TYPE_CHECKING:
    from core.scene import Scene

class TerrainMesh(Component):
 
    def __init__(self, resolution: int = 200):
        Component.__init__(self)
        self.plane = None
        self.resolution = resolution
        
    def Awake(self):
        pass
    
    def Start(self):
        # Create heightmap texture with perlin
        
        #surface = pg.Surface((width, height))
        #pixelArray = pg.PixelArray(surface)
        # self.GeneratePerlinNoise(pixelArray, octaves=2, persistence=0.5, lacunarity=2, seed=1)
        # pg.image.save(pixelArray.surface,'temp.jpeg')
        
        #heightmap = GeneratedTexture(width,height,pixelArray)
        heightmap = Texture('textures/temp2.png', colorMode="RGB")
        width = heightmap.width
        height = heightmap.height
        # Create Plane
        planeObj = Object("plane")
        meshRenderer = self.GenerateMesh(width, height,  self.resolution)
        gl.glPatchParameteri(gl.GL_PATCH_VERTICES, 4)
        meshRenderer.mesh[0].SetDrawMode(Mesh.DrawMode.PATCHES)
        meshRenderer.mesh[0].SetMaterial(Material(Shader("env/terrain/vert", "env/terrain/basic_lit",tessControlShaderName="env/terrain/tess_cont", tessEvalShaderName="env/terrain/tess_eval"), diffuseTex = heightmap, specularTex=heightmap))
        meshRenderer.mesh[0].SetUniformPasser(self.PassUniforms)
        planeObj.AddComponent(meshRenderer)
        self.plane = self.scene.Instantiate(planeObj)
        self.transform.scale = glm.vec3(100,100,100)

    def Update(self):
        self.plane.transform.position = self.transform.position
        self.plane.transform.rotation = self.transform.rotation
        self.plane.transform.scale = self.transform.scale
    

    def GenerateMesh(self, width, height, resolution):
        rez = resolution
        vertices=[]
        colors=[]
        uvs=[]
        triangles = []
        normals = []
        for i in range(rez-1):
            for j in range(rez-1):
                vertices.append([-width/2.0 + width*i/rez, 0.0, -height/2.0 + height*j/rez])
                uvs.append([i / rez, j / rez])# uv

                vertices.append([-width/2.0 + width*(i+1)/rez, 0.0, -height/2.0 + height*j/rez])
                uvs.append([(i+1) / rez, j / rez])# uv

                vertices.append([-width/2.0 + width*i/rez, 0.0, -height/2.0 + height*(j+1)/rez])
                uvs.append([i / rez, (j+1) / rez])# uv

                vertices.append([-width/2.0 + width*(i+1)/rez, 0.0, -height/2.0 + height*(j+1)/rez])
                uvs.append([(i+1) / rez, (j+1) / rez])# uv
            
        # Fill colors with white for length of vertices
        colors = [[1,1,1]] * len(vertices)

        # Fill normals with 0 for length of vertices
        normals = [[0,1,0]] * len(vertices)
        # Fill triangles with 1 to length of vertices
        triangles = [i for i in range(len(vertices))]

        #return Mesh(0, vertices=vertices, triangles=triangles, colors = colors, uvs=uvs)
        mc = MeshCollection()
        m = Mesh(0, vertices=vertices, triangles=triangles, colors = colors, uvs=uvs, normals=normals)
        mc.addMesh(m)
        return ModelRenderer(mc)

    
    def PassUniforms(self, shader: Shader):
        shader.setInt("MIN_TESS_LEVEL", 3)
        shader.setInt("MAX_TESS_LEVEL", 64)
        shader.setFloat("MIN_DISTANCE", 0)
        shader.setFloat("MAX_DISTANCE", 3800 * self.transform.scale.x)

    def GeneratePerlinNoise(self, pixelArray: pg.PixelArray, octaves: int = 1, persistence: float = 0.5, lacunarity: float = 2, seed: int = 1):
        scale = (pixelArray.surface.get_width(), pixelArray.surface.get_height())
        
        noiseMaps = []
        for i in range(octaves):
            noiseMaps.append(PerlinNoise(octaves=i+1, seed=seed))
        
        # 2d array of noise values
        import numpy as np
        perlinData = np.zeros(shape=(scale[0], scale[1]))
            
        for x in range(pixelArray.surface.get_width()):
            for y in range(pixelArray.surface.get_height()):
                currPers = 1
                currScale = scale
                for noiseMap in noiseMaps:
                    val = noiseMap([x / currScale[0], y / currScale[1]]) * currPers  
                    
                    # set value in pixel array
                    perlinData[x][y] = max(min(perlinData[x][y] + val,1),-1)
                    
                    currPers *= persistence
                    currScale = currScale[0]/lacunarity, currScale[1] / lacunarity
                    
        for x in range(pixelArray.surface.get_width()):
            for y in range(pixelArray.surface.get_height()):
                # set value in pixel array
                val = perlinData[x][y]
                # Map range from -1 to 1 to 0 to 255
                val = (val + 1) * 127.5
                valColor = pg.Color((val, val, val, 255))
                pixelArray.surface.set_at((x, y), valColor)