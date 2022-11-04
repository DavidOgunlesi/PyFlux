import pygame as pg
import OpenGL.GL as gl
from core.util import GetRootPathDir

class Texture:
    def __init__(self, path:str, textureRootPath:str="resources/"):
        self.width, self.height = 0, 0
        self.rawTexData = None
        self.textureID = 0
        try:
            # load image
            image = pg.image.load(f'{GetRootPathDir()}/{textureRootPath}{path}')
            image = pg.transform.flip(image, False, True)
            self.width, self.height = image.get_rect().size
            self.rawTexData = pg.image.tostring(image, "RGB")
        except:
            print(f"ERROR: Could not load texture at {path}")
            return

        self.CreateTexture()
        
    def CreateTexture(self):
        if not self.rawTexData:
            return
        
        self.textureID = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureID)
        
        # set the texture wrapping/filtering options
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, self.width, self.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, self.rawTexData)
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        
    def use(self):
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureID)
        
    def free(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        