import os
from typing import List

import OpenGL.GL as gl
import pygame as pg

from core.util import GetRootPathDir


class Texture:
    '''
    The texture class handles the loading of textures and the creation of the texture object
    '''
    def __init__(self, path:str, textureRootPath:str="resources/", rootPath:str=GetRootPathDir(), colorMode = "RGBA", texIDOverride:int=None):
        self.width, self.height = 0, 0
        self.rawTexData = None
        self.textureID = 0
        self.colorMode = colorMode
        path = self.ValidatePath(f'{rootPath}/{textureRootPath}', path)
        self.texIDOverride = texIDOverride
                
        try:
            # load image
            texpath = f'{rootPath}/{textureRootPath}{path}'
            image = pg.image.load(texpath)
            image = pg.transform.flip(image, False, False)
            self.width, self.height = image.get_rect().size
            self.rawTexData = pg.image.tostring(image, colorMode)
        except:
            print(f"ERROR: Could not load texture at {path}")
            return

        self.CreateTexture()
        
    # If file type isnt specified, it will try to load the file with the following extensions in order
    # .png, .jpg, .jpeg, .bmp
    def ValidatePath(self, dir:str, path:str):
        fileExtensions = [".png", ".jpg", ".jpeg", ".bmp"]
        # Check if the path is a valid file
        if not os.path.isfile(path):
            # Check try different path exntensions
            for ext in fileExtensions:
                if not path.endswith(ext):
                    # Check if file exists
                    if os.path.exists(f'{dir}{path}{ext}'):
                        path += ext
                        break
                else:
                    break
        return path
        
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
        #gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)	
        #gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        #gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)
        if self.colorMode == "RGBA":
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.rawTexData)
        else:
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, self.width, self.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, self.rawTexData)

        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        
    def use(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureID)
        pass
        
    def free(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
   
class GeneratedTexture(Texture):
    '''
    Generated Texture handles textures that are generated in code
    '''
    def __init__(self, width:int, height:int, pixelArray:pg.PixelArray):
        # Create image form x and y values
        self.width, self.height = width, height
        self.rawTexData = pg.image.tostring(pixelArray.surface, "RGBA")
        
        self.CreateTexture()

        
class CubeMap(Texture):
    '''
    Cubemap texture is a special texture that is used for skyboxes
    '''
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
        gl.glActiveTexture(gl.GL_TEXTURE30)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.textureID)
        pass
        
    def free(self):
        # dont free cubemap
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, 0)
        pass
        
class InternalTexture(Texture):
    '''
    Internal Texture is a texture that is generated by the engine
    '''
    def __init__(self, textureID:int):
        self.textureID = textureID
        
    def use(self):
        gl.glActiveTexture(gl.GL_TEXTURE0)
        Texture.use(self)