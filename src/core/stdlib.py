from __future__ import annotations

import ctypes
import time
from typing import TYPE_CHECKING, List

import glm
import numpy as np
import OpenGL.GL as gl
import pygame as pg
from pygame.locals import *

from core.component import Component
from core.components.mesh import Mesh
from core.components.sprite import SpriteRenderer
from core.components.transform import Transform
from core.constants import FLOAT_SIZE
from core.material import Material
from core.object import Object
from core.primitives import PRIMITIVE
from core.scene import Scene
from core.shader import Shader
from core.texture import Texture
