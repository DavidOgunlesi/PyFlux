from __future__ import annotations

from typing import TYPE_CHECKING, List

import glm
import numpy as np
import OpenGL.GL as gl
import pygame as pg

from core.component import Component
from core.texture import Texture
from core.components.mesh import Mesh
from core.primitives import PRIMITIVE
from core.material import Material
from core.shader import Shader
from core.components.transform import Transform
from core.components.sprite import SpriteRenderer
from core.scene import Scene
from core.object import Object

import ctypes
import time
from core.constants import FLOAT_SIZE
from pygame.locals import *
from core.component import Component