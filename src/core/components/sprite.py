import glm
from core.texture import Texture
from core.component import Component
from core.components.mesh import Mesh
from core.primitives import PRIMITIVE
from core.shader import Shader
from core.components.modelRenderer import ModelRenderer
class SpriteRenderer(Component):
    def __init__(self, texture: Texture = None):
        self.texture = texture
        self.color = glm.vec4(1,1,1, 0.5)
        self.modelRenderer = None
    
    def Awake(self):
        from core.material import Material
        
        self.modelRenderer = PRIMITIVE.QUAD()
        if not self.GetComponent(ModelRenderer):
            self.AddComponent(self.modelRenderer)
            
        self.modelRenderer.mesh[0].SetCullMode(Mesh.CULLMODE.NONE)
        self.modelRenderer.mesh[0].SetMaterial(Material(Shader("vertex", "sprite/unlit"), self.texture,  self.texture))

    def Update(self):
        self.LookAtCamera()
        self.RenderSprite()
    
    def LookAtCamera(self):
        #self.transform._rotationMat4 = glm.inverse(self.scene.mainCamera.viewMatrix)
        self.transform.LookAt(self.scene.mainCamera.transform.position)
    
    def RenderSprite(self):
        mesh:Mesh = self.GetComponent(ModelRenderer).mesh[0]
        mesh.material.shader.use()
        mesh.material.use()
        
        mesh.material.shader.setVec4("SpriteColor", self.color.to_list())
        
        mesh.material.shader.free()
        mesh.material.free()
    
    def SetSprite(self, texture: Texture):
        self.texture = texture
        
    