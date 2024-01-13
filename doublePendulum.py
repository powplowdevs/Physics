import pygame
import pymunk
from pymunk.body import Body

#Start pygame
pygame.init()

#Make display
HEIGHT = 600
WITDH = 1000
display = pygame.display.set_mode((WITDH,HEIGHT))

#SET FPS
FPS = 50
clock = pygame.time.Clock()

#our pymunk simulation "world" or space
space = pymunk.Space()
space.gravity = (0,-90)

#CONVERT PYGAME CORDS TO PYMUNK CORDS FUNCTION
def convert_cords(point):
    return point[0], WITDH-point[1]

class Ball(): 
    def __init__(self,x,y, vel, size = 10,type="",):
        self.size = size
        #A body
        if type == "s":
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body()
        self.body.position = x,y
        self.body.velocity = vel
        #A shape
        self.shape = pymunk.Circle(self.body,size)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.filter = pymunk.ShapeFilter(group=1)
        #add body and shape to space
        space.add(self.body,self.shape)
    
    def draw(self):
        #show the circle
        x,y = convert_cords(self.body.position)
        pygame.draw.circle(display,(255,0,0),(int(x),int(y)), self.size)

class String():
    def __init__(self, body1,attachment, identifier="body"):
        self.body1 = body1
        if identifier == "body":
            self.body2 = attachment
        elif identifier == "position":
            self.body2 = pymunk.Body(body_type=Body.STATIC)
            self.body2.position = attachment
        #Make pin joint
        joint = pymunk.PinJoint(self.body1,self.body2)
        space.add(joint)
    
    def draw(self):
        pos1 = convert_cords(self.body1.position)
        pos2 = convert_cords(self.body2.position)
        #draw joint
        pygame.draw.line(display, (0,0,0), pos1,pos2, 2)

trail = []
traillen = 50
#GAME FUNCTION
def game():
    ball1 = Ball(400,700,(5,0))
    ball2 = Ball(600,600,(8,0))
    balls = [ball1,ball2]
    string1 = String(ball1.body,(300,750), "position")
    string2 = String(ball1.body,ball2.body)
    while True:
        #check to see if user wants to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


        display.fill((255,255,255))#draw white background

        #trail
        for ball in balls:
            x,y = ball.body.position
            tr = Ball(x, y,(0,0),5,"s")
            if len(trail) > traillen:
                trail.remove(trail[0])
            trail.append(tr)

        #draw
        ball1.draw()
        ball2.draw()
        string1.draw()
        string2.draw()
        for b in trail:
            b.draw()

        #Update display
        pygame.display.update()

        #FPS TICK
        clock.tick(FPS)
        space.step(1/FPS)

#RUN GAME
game()

pygame.quit()