import pygame
import pymunk
import numpy as np
import math

#Start pygame
pygame.init()

#Make display
HEIGHT = 600
WITDH = 600
display = pygame.display.set_mode((WITDH,HEIGHT))

#SET FPS
FPS = 50
clock = pygame.time.Clock()

#our pymunk simulation "world" or space
space = pymunk.Space()

#CONVERT PYGAME CORDS TO PYMUNK CORDS FUNCTION
def convert_cords(point):
    return point[0], WITDH-point[1]

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
    

class Ball(): 
    def __init__(self,x,y, vel, mass, type=""):
        #A body
        if type == "STATIC":
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body()
        self.body.position = x,y
        self.body.velocity = vel
        #A shape
        self.shape = pymunk.Circle(self.body,10)
        self.shape.density = 1
        self.shape.mass = mass
        self.shape.elasticity = 1
        #add body and shape to space
        space.add(self.body,self.shape)
    
    def draw(self):
        #show the circle
        x,y = convert_cords(self.body.position)
        pygame.draw.circle(display,(255,0,0),(int(x),int(y)), 10)


#GAME FUNCTION
def game():
    planet = Ball(300,300,(-70,0),10)
    moon = Ball(300, 350, (10,0), 10)
    while True:
        #check to see if user wants to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        display.fill((255,255,255))#draw white background

        #move objects 
        forcemtp = gforce(planet,moon)
        forceptm = gforce(moon,planet)
        moon.body.velocity += (forcemtp[0]*-50, forcemtp[1]*-50)
        planet.body.velocity += (forceptm[0]*-50, forceptm[1]*-50)

        #draw objects
        planet.draw()
        moon.draw()

        #Update display
        pygame.display.update()

        #FPS TICK
        clock.tick(FPS)
        space.step(1/FPS)

#RUN GAME
game()

pygame.quit()