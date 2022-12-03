import copy

import glm

from core.component import Component
from core.components.mesh import Mesh
from core.components.modelRenderer import ModelRenderer
from core.primitives import PRIMITIVE
from core.shader import Shader
from core.texture import Texture


class SpriteRenderer(Component):
    def Copy(self) -> Component:
        c = SpriteRenderer()
        c.texture = self.texture
        c.color = copy.copy(self.color)
        c.modelRenderer = self.modelRenderer.Copy()
        return c

    def __init__(self, texture: Texture = None):
        Component.__init__(self)
        self.texture = texture
        self.color = glm.vec4(1,1,1, 0.5)
        self.modelRenderer = PRIMITIVE.QUAD()
    
    def Awake(self):
        from core.material import Material
        
        if not self.GetComponent(ModelRenderer):
            self.AddComponent(self.modelRenderer)
            
        self.modelRenderer.meshes[0].SetCullMode(Mesh.CULLMODE.NONE)
        self.modelRenderer.meshes[0].SetMaterial(Material(Shader("vertex", "sprite/unlit"), self.texture,  self.texture))

    def Update(self):
        self.LookAtCamera()
        self.RenderSprite()
    
    def LookAtCamera(self):
        #self.transform._rotationMat4 = glm.inverse(self.scene.mainCamera.viewMatrix)
        self.transform.LookAt(self.scene.mainCamera.transform.position)
    
    def RenderSprite(self):
        mesh:Mesh = self.GetComponent(ModelRenderer).meshes[0]
        mesh.material.shader.use()
        mesh.material.use()
        
        mesh.material.shader.setVec4("SpriteColor", self.color.to_list())
        
        mesh.material.shader.free()
        mesh.material.free()
    
    def SetSprite(self, texture: Texture):
        self.texture = texture
    
    def SetColor(self, color: glm.vec4):
        self.color = color
    