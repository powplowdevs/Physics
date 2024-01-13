import pygame
import pymunk
import numpy as np
import math
import random
import time

#Start pygame
pygame.init()

#Make display
HEIGHT = 600
WITDH = 1000
display = pygame.display.set_mode((WITDH,HEIGHT))

#SET FPS
FPS = 64
clock = pygame.time.Clock()

#our pymunk simulation "world" or space
space = pymunk.Space()

#CONVERT PYGAME CORDS TO PYMUNK CORDS FUNCTION
def convert_cords(point):
    return point[0], HEIGHT-point[1]

def gforce(p1,p2):
    # Calculate the gravitational force exerted on p1 by p2.
    G = 1 # Change to 6.67e-11 to use real-world values.
    # Calculate distance vector between p1 and p2.
    r_vec = p1.body.position-p2.body.position
    # Calculate magnitude of distance vector.
    r_mag = np.linalg.norm(r_vec)
    # Calcualte unit vector of distance vector.
    r_hat = r_vec/r_mag
    # Calculate force magnitude.
    force_mag = G*p1.shape.mass*p2.shape.mass/r_mag**2
    # Calculate force vector.
    force_vec = -force_mag*r_hat
    
    return force_vec


SIZE = 1  
class Ball(): 
    def __init__(self,tag,x,y, vel, mass, type=""):
        #tag
        self.tag = tag
        #A body
        if type == "STATIC":
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body()
        self.body.position = convert_cords((x,y))
        self.body.velocity = vel
        #A shape
        self.shape = pymunk.Circle(self.body,SIZE+(mass*0.1))
        self.shape.density = 1
        self.shape.mass = mass
        self.shape.elasticity = 1
        self.shape.filter = pymunk.ShapeFilter(group=1)
        #add body and shape to space
        space.add(self.body,self.shape)
    
    def draw(self):
        #show the circle
        if self.tag == "sun":
            x,y = convert_cords(self.body.position)
            pygame.draw.circle(display,(255,255,0),(x,y), SIZE+(self.shape.mass*0.1))
        else:
            x,y = convert_cords(self.body.position)
            pygame.draw.circle(display,(self.shape.mass,0,255),(x,y), SIZE+(self.shape.mass*0.1))

#GAME FUNCTION
AMT = 20
def game():
    planets = [Ball(i,random.randint(100,WITDH-100),random.randint(100,HEIGHT-100), (random.uniform(-10,10),random.uniform(-10,10)), random.randint(10,50)) for i in range(AMT)]
    sun = Ball("sun", WITDH/2, HEIGHT/2, (0,0), 100, "STATIC")
    #sun = Ball(100, WITDH-10,HEIGHT-10, (0,0), 100, "STATIC")
    planets.append(sun)
    while True:
        #check to see if user wants to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        display.fill((255,255,255))#draw white background

        #move objects 
        for planet1 in planets:
            for planet2 in planets:
                if planet1.tag != planet2.tag:
                    if planet1.body.position[0] < -100 or planet1.body.position[0] > WITDH+100 or planet1.body.position[1] < 0-100 or planet1.body.position[1] > HEIGHT+100:
                        planets.remove(planet1)
                        #print("removed:", planet1, "it was as pos:", planet1.body.position, "li is now", planets)
                        break
                    else:
                        force = gforce(planet1, planet2)
                        planet1.body.velocity += (force[0]*5, force[1]*5)
                    
    
        #draw objects
        [planet.draw() for planet in planets]
        
        #Update display
        pygame.display.update()
        

        #FPS TICK
        clock.tick(FPS)
        space.step(1/FPS)

#RUN GAME
game()

pygame.quit()