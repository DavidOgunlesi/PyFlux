from __future__ import annotations
from typing import TYPE_CHECKING, List, Type

from core.shader import Shader
from core.texture import Texture

class Material:
    def __init__(self, shader: Shader, texture:Texture):
        self.shader = shader
        self.texture = texture
        
    