from __future__ import annotations
from typing import List, Callable, Tuple, Any, Dict
import pygame as pg

eventTypeDict: Dict[int, PollEvent] = {}
eventQueue: List[PollEvent] = []

class PollEvent:
    def __init__(self, eventType: int, onEvent: Callable, data):
        self.eventType = eventType
        self.onEvent = onEvent
        self.data = data
        self.event = None

def pollEvent(eventType: int, onEvent: Callable, **data):
    if eventType not in eventTypeDict:
        eventQueue.append(PollEvent(eventType, onEvent, data))
        eventTypeDict[eventType] = eventType
    
def ExecuteEvents():
    # for loop through the event queue  
    for event in pg.event.get():
        i = 0
        removeIdxs = []
        eventsToRun: List[PollEvent] = []
        
        # Collect all satisfied events
        for pollEvent in eventQueue:
            if event.type == pollEvent.eventType:
                removeIdxs.append(i)
                pollEvent.event = event
                eventsToRun.append(pollEvent)
            i+=1
            
        # Execute all satisfied events
        for idx, item in enumerate(removeIdxs):
            if item != -1:
                eventQueue.pop(item)
                eventTypeDict.pop(pollEvent.eventType, None)
                pollEvent = eventsToRun[idx]
                pollEvent.onEvent(pollEvent.event, pollEvent.data)
    
    eventTypeDict.clear()
    eventQueue.clear()