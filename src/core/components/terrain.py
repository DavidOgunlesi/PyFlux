from __future__ import annotations

import math
import random
import time
from typing import TYPE_CHECKING, Dict, Tuple

import glm
import numpy as np
import OpenGL.GL as gl
import pygame as pg
from perlin_noise import PerlinNoise

import core.gametime as gametime
import core.input as input
from core.collections.mesh import MeshCollection
from core.component import Component
from core.components.mesh import Mesh
from core.components.modelRenderer import ModelRenderer
from core.fileloader import MeshLoader
from core.material import Material
from core.object import Object
from core.shader import Shader
from core.texture import Texture

if TYPE_CHECKING:
    from core.scene import Scene

class TerrainMesh(Component):
    '''
    TerrainMesh Component is responsible for generating the terrain mesh and storing the heightmap
    Includes creating trees, grass and water
    '''
    def Copy(self) -> Component:
        c = TerrainMesh(self.resolution)
        c.plane = self.plane
        c.timeseed = self.timeseed
        c.waterPlane = self.waterPlane
        c.terrainScale = self.terrainScale
        c.treeChunks = self.treeChunks
        c.chunkNum = self.chunkNum
        c.heightmap = self.heightmap
        c.slopemap = self.slopemap
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
        self.slopemap = None
        self.width = 0
        self.height = 0
        self.treePrefab = Object("tree!!")
        self.modelRenderer = ModelRenderer(MeshLoader.Load("models/tree2"))
        self.modelRenderer.SetShader(Shader("env/tree/vertex", "fragment"))
        self.treePrefab.AddComponent(self.modelRenderer)
        
        #for mesh in self.modelRenderer.meshes:
            #mesh.VAO, mesh.IVA = mesh.GenerateVAO()

        self.modelMatrices = []

    def Awake(self):
        # Create heightmap texture with perlin
        
        #surface = pg.Surface((width, height))
        #pixelArray = pg.PixelArray(surface)
        # self.GeneratePerlinNoise(pixelArray, octaves=2, persistence=0.5, lacunarity=2, seed=1)
        # pg.image.save(pixelArray.surface,'temp.jpeg')
        
        #heightmap = GeneratedTexture(width,height,pixelArray)
        heightmap = Texture('textures/terrain/heightmap.png', colorMode="RGB",)
        self.slopemap = Texture('textures/terrain/slopemap.png', colorMode="RGB",)
        dirt = Texture('textures/grass_seamless_texture_1392.jpg', colorMode="RGBA")
        dirtAlt = Texture('textures/jungle/dirt.jpg', colorMode="RGBA")
        water = Texture('textures/jungle/sand.jpg', colorMode="RGBA")
        rock = Texture('textures/jungle/rock.jpg', colorMode="RGBA")
        grass = Texture('textures/jungle/grass.jpg', colorMode="RGBA")
        sand = Texture('textures/jungle/sand.jpg', colorMode="RGBA")
        grassBladeTexture = Texture('textures/jungle/grassBlade.jpg', colorMode="RGBA")
        tree0 = Texture('textures/trees/treesSprite_00.png', colorMode="RGBA")
        tree1 = Texture('textures/trees/treesSprite_01.png', colorMode="RGBA")
        tree2 = Texture('textures/trees/treesSprite_02.png', colorMode="RGBA")
        tree3 = Texture('textures/trees/treesSprite_03.png', colorMode="RGBA")
        tree4 = Texture('textures/trees/treesSprite_04.png', colorMode="RGBA")
        tree5 = Texture('textures/trees/treesSprite_05.png', colorMode="RGBA")
        tree6 = Texture('textures/trees/treesSprite_06.png', colorMode="RGBA")
        width = heightmap.width
        height = heightmap.height
        scale = 100
        # Create Plane
        planeObj = Object("terrrain plane")
        
        meshRenderer = self.GenerateMesh(width, height,  self.resolution)
        gl.glPatchParameteri(gl.GL_PATCH_VERTICES, 4)
        meshRenderer.meshes[0].SetDrawMode(Mesh.DrawMode.PATCHES)
        mat = Material(Shader("env/terrain/vert", "env/terrain/basic_lit",tessControlShaderName="env/terrain/tess_cont", geomShaderName="env/terrain/geom", tessEvalShaderName="env/terrain/tess_eval"), diffuseTex=dirt, specularTex=rock)

        mat.SetTexture(heightmap, gl.GL_TEXTURE3)
        mat.SetTexture(grass, gl.GL_TEXTURE4)
        mat.SetTexture(sand, gl.GL_TEXTURE5)
        mat.SetTexture(dirtAlt, gl.GL_TEXTURE6)
        mat.SetTexture(water, gl.GL_TEXTURE7)
        mat.SetTexture(self.slopemap, gl.GL_TEXTURE8)
        mat.SetTexture(grassBladeTexture, gl.GL_TEXTURE9)
        meshRenderer.meshes[0].SetMaterial(mat)
        meshRenderer.meshes[0].SetShadowPassShader(Shader("env/terrain/vert", "env/lightmap/null_frag", geomShaderName="env/terrain/geom_lightmap", tessControlShaderName="env/terrain/tess_cont", tessEvalShaderName="env/terrain/tess_eval"))
        meshRenderer.meshes[0].SetUniformPasser(self.PassUniformsTerrain)
        meshRenderer.meshes[0].SetCullMode(Mesh.CULLMODE.NONE)
        planeObj.AddComponent(meshRenderer)

        self.plane = self.scene.Instantiate(planeObj)
        self.plane.transform.scale = glm.vec3(scale,scale,scale)

         # Create Plane
        treeFoliage = Object("tree plane")
        
        meshRenderer = self.GenerateMesh(width, height,  self.resolution)
        gl.glPatchParameteri(gl.GL_PATCH_VERTICES, 4)
        meshRenderer.meshes[0].SetDrawMode(Mesh.DrawMode.PATCHES)
        mat = Material(Shader("env/terrainTrees/vert", "env/terrainTrees/basic_lit",tessControlShaderName="env/terrainTrees/tess_cont", geomShaderName="env/terrainTrees/geom", tessEvalShaderName="env/terrainTrees/tess_eval"), diffuseTex=dirt, specularTex=rock)

        mat.SetTexture(heightmap, gl.GL_TEXTURE3)
        mat.SetTexture(self.slopemap, gl.GL_TEXTURE8)
        mat.SetTexture(tree0, gl.GL_TEXTURE20)
        mat.SetTexture(tree1, gl.GL_TEXTURE21)
        mat.SetTexture(tree2, gl.GL_TEXTURE22)
        mat.SetTexture(tree3, gl.GL_TEXTURE23)
        mat.SetTexture(tree4, gl.GL_TEXTURE24)
        mat.SetTexture(tree5, gl.GL_TEXTURE25)
        mat.SetTexture(tree6, gl.GL_TEXTURE26)
        meshRenderer.meshes[0].SetMaterial(mat)
        meshRenderer.meshes[0].SetShadowPassShader(Shader("env/terrainTrees/vert", "env/lightmap/null_frag", geomShaderName="env/terrainTrees/geom_lightmap", tessControlShaderName="env/terrainTrees/tess_cont", tessEvalShaderName="env/terrainTrees/tess_eval"))
        meshRenderer.meshes[0].SetUniformPasser(self.PassUniformsTerrainTrees)
        meshRenderer.meshes[0].SetCullMode(Mesh.CULLMODE.NONE)
        treeFoliage.AddComponent(meshRenderer)

        treeFoliageInst = self.scene.Instantiate(treeFoliage)
        treeFoliageInst.transform.scale = glm.vec3(scale,scale,scale)

        waterplaneObj = Object("water plane")
        meshRenderer = self.GenerateMesh(width, height,  self.resolution)
        gl.glPatchParameteri(gl.GL_PATCH_VERTICES, 4)
        meshRenderer.meshes[0].SetDrawMode(Mesh.DrawMode.PATCHES)
        mat = Material(Shader("env/water/vert", "env/water/frag",tessControlShaderName="env/terrain/tess_cont", tessEvalShaderName="env/water/tess_eval"))

        meshRenderer.meshes[0].SetMaterial(mat)
        meshRenderer.meshes[0].SetShadowPassShader(Shader("env/water/vert", "env/lightmap/null_frag",tessControlShaderName="env/terrain/tess_cont", tessEvalShaderName="env/water/tess_eval_lightmap"))
        meshRenderer.meshes[0].SetUniformPasser(self.PassUniformsWater)
        waterplaneObj.AddComponent(meshRenderer)

        self.waterPlane = self.scene.Instantiate(waterplaneObj)
        self.waterPlane.transform.scale = glm.vec3(scale,scale,scale)
        self.waterPlane.transform.position = glm.vec3(0,1473/100 * scale,0)

        self.terrainScale = width*scale
        self.heightmap = heightmap
        self.width = width
        self.height = height

        width=self.width//10
        height=self.height//10
        self.subdivision=10
        size = (width//self.subdivision)*(height//self.subdivision)
        self.modelMatrices = [self.GetPoseMatrices(i,self.subdivision, self.modelRenderer.meshes[0], size) for i in range(size)]

    def Update(self):
        # Cunked Trees broke for whatever reason so I'm just going to use instanced trees for now o(≧口≦)o
        # chunkSize = self.terrainScale / self.chunkNum
        # if self.scene.mainCamera.transform.position.y * chunkSize < 8:
        #      self.UpdateChunks()

        # self.PreChunks()
        if input.GetKeyPressed(pg.K_UP):
            self.waterPlane.transform.position += glm.vec3(0,100,0) * gametime.deltaTime

    def UpdateChunks(self):
        for x in range(-1, 1):
            for z in range(-1, 1):
                chunkX, chunkZ = self.GetCurrentChunkNumber(self.scene.mainCamera.transform.position.x, self.scene.mainCamera.transform.position.z)
                chunkX += x
                chunkZ += z
                if (chunkX, chunkZ) not in self.treeChunks:
                    self.GenerateFoliage(chunkX, chunkZ)
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
            inst.transform.position = glm.vec3(x, 100, z)
            modelRenderer: ModelRenderer = inst.FindComponentOfType(ModelRenderer)
            
            
            for mesh in modelRenderer.meshes:
                mesh.SetUniformPasser(self.PassUniformsTree)

            for material in modelRenderer.materials:
                material.SetTexture(self.heightmap, gl.GL_TEXTURE3)
                material.SetTexture(self.slopemap, gl.GL_TEXTURE4)
            
            modelRenderer.modelMatrices = self.modelMatrices

        self.pretreeChunks.clear()

    def GetPoseMatrices(self, i: int, subdivision:int, c:Component, size: int):
        # Create vectors in a grid based on i index, with spacing
        spacing = subdivision
        vec = glm.vec3(((i+1) % math.sqrt(size)) * spacing, 0, ( math.floor(i / math.sqrt(size))) * spacing)
        randomRotation = glm.vec3(-90, random.randint(0,360), 0)
        scale = random.uniform(0.5,1.5)
        randomScale = glm.vec3(scale, scale, scale)
        maxOffset = spacing/2
        randomOffset = glm.vec3(random.uniform(-maxOffset,maxOffset), 0, random.uniform(-maxOffset,maxOffset))

        poseMtx = c.transform.GetPoseMatrix(translation=vec+randomOffset, rotation=randomRotation, scale=randomScale)
        mat4Arr = np.array(poseMtx, dtype=np.float32)
        mat4Arr = mat4Arr.flatten()
        return mat4Arr

    def PassUniformsTerrain(self, shader: Shader):
        shader.setInt("MIN_TESS_LEVEL", 4)
        shader.setInt("MAX_TESS_LEVEL", 64)
        shader.setFloat("MIN_DISTANCE", 100)
        shader.setFloat("MAX_DISTANCE", 3080)
        shader.setFloat("time", self.timeseed)
        shader.setFloat("gametime", gametime.time)
        shader.setFloat("terrainscale", self.terrainScale)
        shader.setInt("terrainTiling", 4000)

    def PassUniformsTerrainTrees(self, shader: Shader):
        shader.setInt("MIN_TESS_LEVEL", 1)
        shader.setInt("MAX_TESS_LEVEL", 64)
        shader.setFloat("MIN_DISTANCE", 0)
        shader.setFloat("MAX_DISTANCE", 10800)
        shader.setFloat("time", self.timeseed)
        shader.setFloat("gametime", gametime.time)
        shader.setFloat("terrainscale", self.terrainScale)
        shader.setInt("terrainTiling", 4000)
        #for idx in range(7):
        #    shader.setInt(f"treeTextures[{idx}]", 20+idx)

    def PassUniformsWater(self, shader: Shader):
        shader.setInt("MIN_TESS_LEVEL", 1)
        shader.setInt("MAX_TESS_LEVEL", 32)
        shader.setFloat("MIN_DISTANCE", 100)
        shader.setFloat("MAX_DISTANCE", 3080)
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