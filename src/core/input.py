import pygame as pg

import core.eventsystem as eventsystem

pressed_once = []
__mouseWheelDelta = (0,0)

def GetKeyDown(key:int):
    eventsystem.pollEvent(pg.KEYUP, KeyUpEvent, key = key)
    keys = pg.key.get_pressed()
    if keys[key] and key not in pressed_once:
        pressed_once.append(key)
        return True
    
def GetMouseWheel():
    global __mouseWheelDelta
    eventsystem.pollEvent(pg.MOUSEWHEEL, MouseWheelEvent)
    result = __mouseWheelDelta
    __mouseWheelDelta = (0,0)
    return result
    
def GetKeyPressed(key:int) -> bool:
    keys = pg.key.get_pressed()
    if keys[key]:
        return True
        
def KeyUpEvent(event, data):
    key = data["key"]
    if event.key == key:
        pressed_once.remove(key)
        
        
def MouseWheelEvent(event, data):
    global __mouseWheelDelta
    __mouseWheelDelta = (event.x, event.y)