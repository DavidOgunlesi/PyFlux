from __future__ import annotations
import glm
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.runtime import Runtime
    from core.shader import Shader
    
GLOBAL_TRANSFORM = glm.mat4(1)
GLOBAL_RENDERSHADER: Shader = None
CURRENTRENDERCONTEXT:Runtime = None