from __future__ import annotations

from typing import TYPE_CHECKING

import glm

from core.component import Component
from core.components.mesh import Mesh
from core.components.modelRenderer import ModelRenderer
from core.primitives import PRIMITIVE
from core.shader import Shader
from core.texture import CubeMap

if TYPE_CHECKING:
    from core.material import Material

class Skybox(Component):

    def Copy(self) -> Component:
        c = Skybox(self.resourcepath, self.faces)
        c.material = self.material
        return c

    def __init__(self, resourcepath, faces):
        Component.__init__(self)
        self.resourcepath = resourcepath
        self.faces = faces
        self.material:Material = None
    
    def Start(self):
        from core.material import Material
        
        modelRenderer = PRIMITIVE.UNITCUBE()
        if not self.GetComponent(ModelRenderer):
            self.AddComponent(modelRenderer)
        
        
        cubemap = CubeMap(self.resourcepath, self.faces)
        
        modelRenderer.meshes[0].SetCullMode(Mesh.CULLMODE.BACK)
        modelRenderer.meshes[0].SetMaterial(Material(Shader("env/skybox/vertex", "env/skybox/fragment"), cubemap, cubemap))
        self.material =  modelRenderer.meshes[0].material
        modelRenderer.meshes[0].SetDepthWriting(False)
        modelRenderer.meshes[0].OverrideViewMtx()
        modelRenderer.meshes[0].castShadows = False
        #modelRenderer.mesh[0].IgnoreCameraDistance(True)
        
    def Update(self):
        modelRenderer:ModelRenderer = self.GetComponent(ModelRenderer)
        modelRenderer.meshes[0].viewMtxOverrideValue = glm.mat4(glm.mat3(self.scene.mainCamera.viewMatrix))