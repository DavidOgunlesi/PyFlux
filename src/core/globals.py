from __future__ import annotations

from typing import TYPE_CHECKING

import glm

if TYPE_CHECKING:
    from core.runtime import Renderer
    from core.shader import Shader
    
GLOBAL_TRANSFORM = glm.mat4(1)
GLOBAL_RENDERSHADER: Shader = None
CURRENTRENDERCONTEXT:Renderer = None
WINDOW_DIMENSIONS = (0,0)