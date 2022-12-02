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

class Boid(Component):

    global_boids: List[Boid] = []
    #Max acceleration and speed
    Max_Acceleration = 5.0
    Max_Dumper = 3.0
    Max_Velocity = 3.0

    # Magnitudes
    Magnitude_Cohesion = .1
    Magnitude_Separation = 10
    Magnitude_Alignment = 10

    #Range
    Range_Cohesion = 40
    Range_Separation = 10
    Range_Alignment = 40

    def Copy(self) -> Component:
        c = Boid()
        c.sprite = self.sprite
        return c
        
    def __init__(self):
        Component.__init__(self)
        self.sprite = "textures/bird.png"
        self.initialDirection = glm.vec3(0, 0, 0)
        self.viewAngle = 100
        
    def Awake(self):
        if not self.GetComponent(SpriteRenderer):
            self.AddComponent(SpriteRenderer(Texture(self.sprite)))
        pass
    
    def Start(self):
        self.currentDirection = glm.vec3(random.randint(-1, 1), random.randint(-1, 1), random.randint(-1, 1))
        sprR: SpriteRenderer = self.GetComponent(SpriteRenderer)   
        sprR.SetSprite(Texture(self.sprite)) 
        sprR.SetColor(glm.vec4(0, 0, 0, 1))
        sprR.modelRenderer.meshes[0].castShadows = False
        Boid.global_boids.append(self)
        self.transform.scale = glm.vec3(4.5, 4.5, 4.5)
        self.transform.position += glm.vec3(random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100))
    
    def Update(self):
        ###############################################################################
        # Find its neighbor boids that are in the range and run the following methods:
        ###############################################################################
        neighbours = self.GetNeighbours(Boid.Range_Cohesion)
        # Run Cohesion method and get the vector value
        cohesion = self.Cohere(neighbours) * Boid.Magnitude_Cohesion
        neighbours = self.GetNeighbours(Boid.Range_Separation)
        # Run Separation method and get the vector value
        separation = self.Separate(neighbours) * Boid.Magnitude_Separation
        neighbours = self.GetNeighbours(Boid.Range_Alignment)
        # Run Alignment method and get the vector value
        alignment = self.Align(neighbours) * Boid.Magnitude_Alignment

        # Combine the Cohesion, Separation and Alignment vectors as an acceleration
        randV = 6.0
        randomizeV = glm.vec3(random.randint(-randV, randV), random.randint(-randV, randV), random.randint(-randV, randV))
        acceleration = cohesion + separation + alignment + randomizeV
        acceleration = glm.clamp(acceleration, 0, Boid.Max_Acceleration)
        # Add acceleration to its vector
        damp = 0.45
        self.currentDirection = (self.currentDirection + acceleration) * damp
        self.currentDirection = glm.clamp(self.currentDirection, 0, Boid.Max_Velocity)

        # Update position
        self.transform.position += self.currentDirection
    
    def angleBetween(self, a: glm.vec3 ,b : glm.vec3, origin : glm.vec3):
        da = glm.normalize(a-origin)
        db = glm.normalize(b-origin)
        return glm.degrees(glm.acos(glm.dot(da, db)))
        


    def GetNeighbours(self, range: float) -> List[Boid]:
        neighbours = []
        for boid in Boid.global_boids:
            if boid == self:
                continue
            if glm.length(self.transform.position - boid.transform.position) < range and self.angleBetween(self.currentDirection, boid.currentDirection, self.transform.position) < self.viewAngle:
                neighbours.append(boid)
        return neighbours


    def Cohere(self, neighbours: List[Boid]):
        # If there are no neighbors, return 0 vector.
        if len(neighbours) == 0:
            return glm.vec3(0, 0, 0)

        # Find the center position of its neighbors,
        # then find a new vector from this boid’s position to this center position.
        center = glm.vec3(0, 0, 0)
        for neighbour in neighbours:
            center += neighbour.transform.position

        center /= len(neighbours)
        direction = glm.normalize(center - self.transform.position)

        return direction

    def Separate(self, neighbours: List[Boid]):
        # If there are no neighbors, return 0 vector.
        if len(neighbours) == 0:
            return glm.vec3(0, 0, 0)

        sumDirection = glm.vec3(0, 0, 0)
        # For each of its neighbor boid,
        # find a vector directing from each of its neighbor boid’s position to this boid’s position.
        for neighbour in neighbours:
            direction = self.transform.position - neighbour.transform.position

            #If the above vector is greater than 0,
            # the force should be inversely proportional to the distance.
            if glm.length(direction) > 0:
                direction += glm.normalize(direction) / glm.length(direction)


        return glm.normalize(sumDirection)


    def Align(self, neighbours: List[Boid]):
        # If there are no neighbors, finish here and return 0 vector.
        if len(neighbours) == 0:
            return glm.vec3(0, 0, 0)

        #For each of its neighbor boid,
        # get its current vector and combine all to find the average vector within its neighbors
        sumDirection = glm.vec3(0, 0, 0)
        for neighbour in neighbours:
            sumDirection += neighbour.currentDirection

        return glm.normalize(sumDirection)