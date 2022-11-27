import pygame as pg
import OpenGL.GL as gl
from core.util import GetRootPathDir
import os
from typing import List

 

class Texture:
    def __init__(self, path:str, textureRootPath:str="resources/", rootPath:str=GetRootPathDir()):
        self.width, self.height = 0, 0
        self.rawTexData = None
        self.textureID = 0
        try:
            # load image
            image = pg.image.load(f'{rootPath}/{textureRootPath}{path}')
            image = pg.transform.flip(image, False, False)
            self.width, self.height = image.get_rect().size
            self.rawTexData = pg.image.tostring(image, "RGBA")
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
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)	
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.rawTexData)
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        
    def use(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureID)
        
    def free(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        
class CubeMap(Texture):
    def __init__(self, path:str, faces:List[str], textureRootPath:str="resources/"):
        self.width, self.height = 0, 0
        self.rawTexData = []
        self.textureID = 0
        # try:
        path = f'{GetRootPathDir()}/{textureRootPath}{path}'
        #for subdir, dirs, files in os.walk(path):
            #for idx, file in enumerate(files):
                #subpath = os.path.join(subdir, file)
        for idx in range(0, len(faces)):  
            image = pg.image.load(f"{path}/{faces[idx]}")
            image = pg.transform.flip(image, False, False)
            self.width, self.height = image.get_rect().size
            self.rawTexData.append(pg.image.tostring(image, "RGB"))
                
        self.CreateCubemap()
        # except:
        #     print(f"ERROR: Could not load cubemap at {path}")
        #     return
        
    def CreateCubemap(self):
        if not self.rawTexData:
            return
        
        self.textureID = gl.glGenTextures(1)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.textureID)
        for idx, data in enumerate(self.rawTexData):
            gl.glTexImage2D(gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X + idx, 0, gl.GL_RGB, self.width, self.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, data)
            
        # set the texture wrapping/filtering options
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri( gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)	
        gl.glTexParameteri( gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri( gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, 0)
        
    def use(self):
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.textureID)
        pass
        
    def free(self):
        # dont free cubemap
        #gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, 0)
        pass
        
              