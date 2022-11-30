from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, List, Dict, Any, Tuple
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
import core.input as input
import numpy as np
from core.fileloader import MeshLoader
import math
import random


import threading
import time

if TYPE_CHECKING:
    from core.scene import Scene

class TerrainMesh(Component):
    def Copy(self) -> Component:
        c = TerrainMesh(self.resolution)
        c.plane = self.plane
        c.timeseed = self.timeseed
        c.waterPlane = self.waterPlane
        c.terrainScale = self.terrainScale
        c.treeChunks = self.treeChunks
        c.chunkNum = self.chunkNum
        c.heightmap = self.heightmap
        c.width = self.width
        c.height = self.height
        c.treePrefab = self.treePrefab.Copy()
        return c
        
    def __init__(self, resolution: int = 200):
        Component.__init__(self)
        self.plane = None
        self.resolution = resolution
        self.timeseed = gametime.time
        self.waterPlane = None
        self.terrainScale = 0
        self.pretreeChunks: Dict[Tuple[int, int], ModelRenderer] = {}
        self.treeChunks: Dict[Tuple[int, int], ModelRenderer] = {}
        self.chunkNum = 1000
        self.heightmap = None
        self.width = 0
        self.height = 0
        self.treePrefab = Object("tree")
        modelRenderer = ModelRenderer(MeshLoader.Load("models/tree2"))
        self.treePrefab.AddComponent(modelRenderer)
    
    def Awake(self):
        # Create heightmap texture with perlin
        
        #surface = pg.Surface((width, height))
        #pixelArray = pg.PixelArray(surface)
        # self.GeneratePerlinNoise(pixelArray, octaves=2, persistence=0.5, lacunarity=2, seed=1)
        # pg.image.save(pixelArray.surface,'temp.jpeg')
        
        #heightmap = GeneratedTexture(width,height,pixelArray)
        heightmap = Texture('textures/temp2.png', colorMode="RGB",)
        dirt = Texture('textures/grass_seamless_texture_1392.jpg', colorMode="RGBA")
        dirtAlt = Texture('textures/jungle/dirt.jpg', colorMode="RGBA")
        water = Texture('textures/jungle/sand.jpg', colorMode="RGBA")
        rock = Texture('textures/jungle/rock.jpg', colorMode="RGBA")
        grass = Texture('textures/jungle/grass.jpg', colorMode="RGBA")
        sand = Texture('textures/jungle/sand.jpg', colorMode="RGBA")
        width = heightmap.width
        height = heightmap.height

        # Create Plane
        planeObj = Object("terrrain plane")
        
        meshRenderer = self.GenerateMesh(width, height,  self.resolution)
        gl.glPatchParameteri(gl.GL_PATCH_VERTICES, 4)
        meshRenderer.meshes[0].SetDrawMode(Mesh.DrawMode.PATCHES)
        mat = Material(Shader("env/terrain/vert", "env/terrain/basic_lit",tessControlShaderName="env/terrain/tess_cont", tessEvalShaderName="env/terrain/tess_eval"), diffuseTex=dirt, specularTex=rock)

        mat.SetTexture(heightmap, gl.GL_TEXTURE3)
        mat.SetTexture(grass, gl.GL_TEXTURE4)
        mat.SetTexture(sand, gl.GL_TEXTURE5)
        mat.SetTexture(dirtAlt, gl.GL_TEXTURE6)
        mat.SetTexture(water, gl.GL_TEXTURE7)

        meshRenderer.meshes[0].SetMaterial(mat)
        meshRenderer.meshes[0].SetUniformPasser(self.PassUniforms)
        planeObj.AddComponent(meshRenderer)

        self.plane = self.scene.Instantiate(planeObj)
        self.plane.transform.scale = glm.vec3(100,100,100)

        waterplaneObj = Object("water plane")
        meshRenderer = self.GenerateMesh(width, height,  self.resolution)
        gl.glPatchParameteri(gl.GL_PATCH_VERTICES, 4)
        meshRenderer.meshes[0].SetDrawMode(Mesh.DrawMode.PATCHES)
        mat = Material(Shader("env/water/vert", "env/water/frag",tessControlShaderName="env/terrain/tess_cont", tessEvalShaderName="env/water/tess_eval"))

        meshRenderer.meshes[0].SetMaterial(mat)
        meshRenderer.meshes[0].SetUniformPasser(self.PassUniformsWater)
        waterplaneObj.AddComponent(meshRenderer)

        self.waterPlane = self.scene.Instantiate(waterplaneObj)
        self.waterPlane.transform.scale = glm.vec3(100,100,100)
        self.waterPlane.transform.position = glm.vec3(0,1473,0)

        self.terrainScale = width*100
        self.heightmap = heightmap
        self.width = width
        self.height = height


    def Update(self):
        for x in range(-1, 1):
            for z in range(-1, 1):
                chunkX, chunkZ = self.GetCurrentChunkNumber(self.scene.mainCamera.transform.position.x, self.scene.mainCamera.transform.position.z)
                chunkX += x
                chunkZ += z
                if (chunkX, chunkZ) not in self.treeChunks:
                    self.GenerateFoliage(chunkX, chunkZ)
                    #self.treeChunks[(chunkX, chunkZ)] = self.GenerateFoliage(chunkX, chunkZ, self.heightmap, width=self.width//10, height=self.height//10, subdivision=10)
                    pass

        # remove chunks that are too far away
        destoryBuffer = []
        for chunk in self.treeChunks:
            currChunk = self.GetCurrentChunkNumber(self.scene.mainCamera.transform.position.x, self.scene.mainCamera.transform.position.z)
            if abs(chunk[0] - currChunk[0]) > 2 or abs(chunk[1] - currChunk[1]) > 2:
                # Delete mesh
                obj: Object = self.treeChunks[chunk]
                obj.Destroy()
                destoryBuffer.append(chunk)

        for chunk in destoryBuffer:
            del self.treeChunks[chunk]

        self.PreChunks()
        if input.GetKeyPressed(pg.K_UP):
            self.waterPlane.transform.position += glm.vec3(0,100,0) * gametime.deltaTime

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

    def GetCurrentChunkNumber(self, x, z):
        # Split terrain into chunks
        chunkSize = self.terrainScale / self.chunkNum
        chunkX = x // chunkSize
        chunkZ = z // chunkSize
        return chunkX, chunkZ

    def ChunkToPosition(self, chunkX, chunkZ):
        chunkSize = self.terrainScale / self.chunkNum
        return chunkX * chunkSize, chunkZ * chunkSize

    def GenerateFoliage(self, chunkX, chunkZ):
        start = time.time()
        self.scene.InstantiateThreaded(self.treePrefab, lambda obj: self.OnTerrainInstantiated(obj, chunkX, chunkZ))
        #print("Instantiate time: ", time.time() - start)
        start = time.time()

    def OnTerrainInstantiated(self, inst, chunkX, chunkZ):
        self.pretreeChunks[(chunkX, chunkZ)] = inst

    def PreChunks(self):
        for chunkX, chunkZ in self.pretreeChunks:
            
            inst = self.pretreeChunks[(chunkX, chunkZ)]
            self.treeChunks[(chunkX, chunkZ)] = inst

            x, z = self.ChunkToPosition(chunkX, chunkZ)
            offset = glm.vec3(x, 0, z)
            modelRenderer: ModelRenderer = inst.FindComponentOfType(ModelRenderer)
            modelRenderer.SetShader(Shader("env/tree/vertex", "fragment"))

            for mesh in modelRenderer.meshes:
                mesh.SetUniformPasser(self.PassUniformsTree)

            for material in modelRenderer.materials:
                material.SetTexture(self.heightmap, gl.GL_TEXTURE3)

            width=self.width//10
            height=self.height//10
            subdivision=10
            size = (width//subdivision)*(height//subdivision)
            modelRenderer.modelMatrices = np.array([self.GetPoseMatrices(i,subdivision, offset, modelRenderer.meshes[0], size) for i in range(size)])

        self.pretreeChunks.clear()

    def GetPoseMatrices(self, i: int, subdivision:int, offset: glm.vec3, c:Component, size: int):
        # Create vectors in a grid based on i index, with spacing
        spacing = subdivision
        vec = glm.vec3(((i+1) % math.sqrt(size)) * spacing, 0, ( math.floor(i / math.sqrt(size))) * spacing)
        randomRotation = glm.vec3(-90, random.randint(0,360), 0)
        scale = random.uniform(0.5,1.5)
        randomScale = glm.vec3(scale, scale, scale)
        maxOffset = spacing/2
        randomOffset = glm.vec3(random.uniform(-maxOffset,maxOffset), 0, random.uniform(-maxOffset,maxOffset))
        poseMtx = c.transform.GetPoseMatrix(translation=vec+randomOffset+offset, rotation=randomRotation, scale=randomScale)
        return poseMtx

    def PassUniforms(self, shader: Shader):
        shader.setInt("MIN_TESS_LEVEL", 3)
        shader.setInt("MAX_TESS_LEVEL", 64)
        shader.setFloat("MIN_DISTANCE", 0)
        shader.setFloat("MAX_DISTANCE", 3800 * self.transform.scale.x)
        shader.setFloat("time", self.timeseed)

    def PassUniformsWater(self, shader: Shader):
        shader.setInt("MIN_TESS_LEVEL", 3)
        shader.setInt("MAX_TESS_LEVEL", 64)
        shader.setFloat("MIN_DISTANCE", 0)
        shader.setFloat("MAX_DISTANCE", 3800 * self.transform.scale.x)
        shader.setFloat("time", gametime.time)    

    def PassUniformsTree(self, shader: Shader):
        shader.setFloat("terrainscale", self.terrainScale)

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