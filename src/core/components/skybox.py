from core.component import Component
from core.shader import Shader
from core.components.modelRenderer import ModelRenderer
from core.primitives import PRIMITIVE
from core.components.mesh import Mesh
from core.texture import CubeMap
import glm

class Skybox(Component):
    def __init__(self, resourcepath, faces):
        self.resourcepath = resourcepath
        self.faces = faces
        self.material = None
    
    def Start(self):
        from core.material import Material
        from core.texture import Texture
        
        modelRenderer = PRIMITIVE.UNITCUBE()
        if not self.GetComponent(ModelRenderer):
            self.AddComponent(modelRenderer)
        
        
        cubemap = CubeMap(self.resourcepath, self.faces)
        
        modelRenderer.mesh[0].SetCullMode(Mesh.CULLMODE.BACK)
        modelRenderer.mesh[0].SetMaterial(Material(Shader("env/skybox/vertex", "env/skybox/fragment"), cubemap, cubemap))
        self.material =  modelRenderer.mesh[0].material
        modelRenderer.mesh[0].SetDepthWriting(False)
        modelRenderer.mesh[0].OverrideViewMtx()
        modelRenderer.mesh[0].castShadows = False
        #modelRenderer.mesh[0].IgnoreCameraDistance(True)
    def Update(self):
        pass
        modelRenderer:ModelRenderer = self.GetComponent(ModelRenderer)
        modelRenderer.mesh[0].viewMtxOverrideValue = glm.mat4(glm.mat3(self.scene.mainCamera.viewMatrix))