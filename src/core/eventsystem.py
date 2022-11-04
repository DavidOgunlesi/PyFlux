from __future__ import annotations
from typing import List, Callable, Tuple, Any
import pygame as pg

eventQueue: List[int] = []

def pollEvent(event: int, onEvent: Callable):
    eventQueue.append((event, onEvent))
    
def ExecuteEvents():
    # for loop through the event queue  
    for event in pg.event.get():
        i = 0
        removeIdxs = []
        eventsToRun: List[Tuple[Callable, Any]] = []
        for eventType, onEvent in eventQueue:
            if event.type == eventType:
                removeIdxs.append(i)
                eventsToRun.append((onEvent, event))
            i+=1
            
        for idx, item in enumerate(removeIdxs):
            if item != -1:
                eventQueue.pop(item)
                callback, event = eventsToRun[idx]
                callback(event)
    
    eventQueue.clear()