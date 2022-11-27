import glm
from core.shader import Shader

GLOBAL_TRANSFORM = glm.mat4(1)
GLOBAL_RENDERSHADER: Shader = None
CURRENTRENDERCONTEXT = None