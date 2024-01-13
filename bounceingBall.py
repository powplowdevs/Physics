import pygame
import pymunk
from pymunk import shape_filter
from pymunk.shapes import Segment
import colorsys

#Start pygame
pygame.init()

#Make display
HEIGHT = 500
WITDH = 500
display = pygame.display.set_mode((WITDH,HEIGHT))

#SET FPS
FPS = 80
clock = pygame.time.Clock()

#our pymunk simulation "world" or space
space = pymunk.Space()
#gravity
space.gravity = 0,-1000,


class Ball(): 
    def __init__(self):
        #A body
        self.body = pymunk.Body()
        self.body.position = 250,450
        #A shape
        self.shape = pymunk.Circle(self.body,10)
        self.shape.density = 1
        self.shape.elasticity = 1
        #add body and shape to space
        space.add(self.body,self.shape)
    
    def draw(self):
        #show the circle
        x,y = convert_cords(self.body.position)
        pygame.draw.circle(display,(255,0,0),(int(x),int(y)), 10)

class Floor():
    def __init__(self):
        #floor or segment or line segment or line. any one tbh
        self.segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.segment_shape = pymunk.Segment(self.segment_body,(0,250), (500, 50), 5)
        self.segment_shape.elasticity = 1
        #add floor to space
        space.add(self.segment_body,self.segment_shape)
    def draw(self):
        #show floor
        pygame.draw.line(display, (0,0,0), convert_cords(self.segment_shape._get_a()), convert_cords(self.segment_shape._get_b()), 5)


#CONVERT PYGAME CORDS TO PYMUNK CORDS FUNCTION
def convert_cords(point):
    return point[0], WITDH-point[1]

#GAME FUNCTION
def game():
    ball = Ball()
    #ball2 = Ball()
    #ball2.body.position = 250,440
    #ball2.shape.density = 1
    floor = Floor()
    while True:
        #check to see if user wants to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        display.fill((255,255,255))#draw white background

        #draw objects
        ball.draw()
#        ball2.draw()
        floor.draw()

        print(ball.body.position)

        #Update display
        pygame.display.update()

        #FPS TICK
        clock.tick(FPS)
        space.step(1/FPS)
        

#RUN GAME
game()

pygame.quit()