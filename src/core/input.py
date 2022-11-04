import pygame as pg
import core.eventsystem as eventsystem

def GetKey(key:int):
    eventsystem.pollEvent(pg.KEYDOWN, KeyEvent)
    # for loop through the event queue  
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == key:
                return True
            
def KeyEvent(event):
    pass