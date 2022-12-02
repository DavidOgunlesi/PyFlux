from __future__ import annotations
from typing import TYPE_CHECKING, List
from core.component import Component
import glm
from core.components.sprite import SpriteRenderer
from core.texture import Texture
import random
if TYPE_CHECKING:
    from scene import Scene
    from core.object import Object
    from components.transform import Transform

from pygame import mixer
from core.util import GetRootPathDir
import os
class AudioClip:
    def __init__(self, path: str, resourcesRootPath:str="resources/", rootPath:str=GetRootPathDir()):
        path = self.ValidatePath(f'{rootPath}/{resourcesRootPath}', path)
        self.path = f'{rootPath}/{resourcesRootPath}{path}'
        self.audio = None
        self.sound = mixer.Sound(self.path)

     # If file type isnt specified, it will try to load the file with the following extensions in order
    # .wav .mp3
    def ValidatePath(self, dir:str, path:str):
        fileExtensions = [".wav", ".mp3"]
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

class AudioSource(Component):
    mixer.init()
    def Copy(self) -> Component:
        c = AudioSource()
        c.audioClip = self.audioClip
        c.playOnAwake = self.playOnAwake
        c.loop = self.loop
        c.attenutionFactor = self.attenutionFactor
        c.attenutionOffset = self.attenutionOffset
        c.volume = self.volume
        c.channel = self.channel
        return c
        
    def __init__(self, clip: AudioClip = None, channel: int = 0):
        Component.__init__(self)
        self.audioClip = clip
        self.playOnAwake = False
        self.loop = True
        self.attenutionFactor = None
        self.attenutionOffset = 0
        self.volume = 1
        self.channel = channel
        
    def Awake(self):
        #Load audio file
        #mixer.Channel(self.channel).load(self.audioClip.path)

        if self.playOnAwake:
            if self.loop:
                mixer.Channel(self.channel).play(self.audioClip.sound, -1)
            else:
                mixer.Channel(self.channel).play(self.audioClip.sound)
    def Update(self):
        if self.attenutionFactor != None:
            mixer.Channel(self.channel).set_volume((self.attenutionFactor/max(abs(self.scene.mainCamera.transform.position.y+self.attenutionOffset), 0.0001)) *  self.volume)


    def Play(self):
        if self.loop:
                mixer.Channel(self.channel).play(self.audioClip.sound, -1)
        else:
            mixer.Channel(self.channel).play(self.audioClip.sound)

    def Stop(self):
        mixer.Channel(self.channel).stop()

    def Pause(self):
        mixer.Channel(self.channel).pause()

    def SetVolume(self, volume: float):
        self.volume = volume
        mixer.Channel(self.channel).set_volume(volume)

    def SetAttenution(self, factor: float = 1, offset: float = 0):
        self.attenutionFactor = factor
        self.attenutionOffset = offset
    