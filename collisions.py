import pygame
import pymunk
import random

#Start pygame
pygame.init()

#Make display
HEIGHT = 500
WITDH = 500
display = pygame.display.set_mode((WITDH,HEIGHT))

#SET FPS
FPS = 50
clock = pygame.time.Clock()

#our pymunk simulation "world" or space
space = pymunk.Space()
space.gravity = 0,-100

#Game vars
balls = []
ball_life = 160
FORCE = -5
tick = 0

#CONVERT PYGAME CORDS TO PYMUNK CORDS FUNCTION
def convert_cords(point):
    return point[0], WITDH-point[1]

class Ball(): 
    def __init__(self,x,y, collision_type, vel, color=(255,0,0), life=0):
        #A body
        self.body = pymunk.Body()
        self.body.position = x,y
        self.body.velocity = vel
        self.color = color
        self.life = life
        #A shape
        self.shape = pymunk.Circle(self.body,10)
        self.shape.density = 1
        self.shape.elasticity = 0.3
        #collisions
        self.shape.collision_type = collision_type 
        #add body and shape to space
        space.add(self.body,self.shape)
    
    def draw(self):
        #show the circle
        self.life += 1
        if self.life >= ball_life:
            try:
                space.remove(self.body,self.shape)
            except:
                pass
        else:
            x,y = convert_cords(self.body.position)
            pygame.draw.circle(display,self.color,(int(x),int(y)), 10)

class Player(): 
    def __init__(self,x,y, vel, color=(0,0,255)):
        #A body
        self.body = pymunk.Body()
        self.body.position = x,y
        self.body.velocity = vel
        self.color = color
        #A shape
        self.shape = pymunk.Circle(self.body,10)
        self.shape.density = 1
        self.shape.elasticity = 0.5
        #collisions
        self.shape.collision_type = 1 
        #add body and shape to space
        space.add(self.body,self.shape)
    
    def draw(self):
        #show the circle
        x,y = convert_cords(self.body.position)
        pygame.draw.circle(display,self.color,(int(x),int(y)), 10)
        
        
    def fly(self):
        if self.body.velocity[0] < 150 and self.body.velocity[1] < 150 and self.body.velocity[0] > -150 and self.body.velocity[1] > -150:
            self.body.velocity += (self.body.velocity[0],self.body.velocity[1]+1)
    def steer(self,direction):
        if direction: #right
            if self.body.velocity[0] < 150 and self.body.velocity[1] < 150 and self.body.velocity[0] > -150 and self.body.velocity[1] > -150:
                self.shape.body.apply_force_at_local_point((-400, 0), (100, 0))
        else: #left
            if self.body.velocity[0] < 150 and self.body.velocity[1] < 150 and self.body.velocity[0] > -150 and self.body.velocity[1] > -150:
                self.shape.body.apply_force_at_local_point((400, 0), (100, 0))
    def brake(self):
        self.shape.body.apply_force_at_local_point((0, -400), (0, -100))

class Line():
    def __init__(self, p1,p2):
        #floor or segment or line segment or line. any one tbh
        self.segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.segment_shape = pymunk.Segment(self.segment_body,p1,p2, 5)
        self.segment_shape.elasticity = 1
        #collisions
        self.segment_shape.collision_type = 3
        #add floor to space
        space.add(self.segment_body,self.segment_shape)
    def draw(self):
        #show floor
        pygame.draw.line(display, (0,0,0), convert_cords(self.segment_shape._get_a()), convert_cords(self.segment_shape._get_b()), 5)


def player_collide(arbiter, space, data):
    print("Player hit")
def floor_collide(arbiter, space, data):
    pass


#GAME FUNCTION
def game():
    global tick
    
    balls = [Ball(random.randint(30,WITDH-30),HEIGHT+30, 2,(0,FORCE))]
    floor = Line((0,10),(500,10))
    right_wall = Line((500,0),(500,HEIGHT+100))
    left_wall = Line((0,0),(0,HEIGHT+100))
    roof = Line((HEIGHT+50,0),(HEIGHT+50,HEIGHT+100))
    player = Player(WITDH/2,30,(0,0))
    
    #collisions handler
    player_handler = space.add_collision_handler(1,2) 
    player_handler.separate = player_collide
    floor_handler = space.add_collision_handler(2,3) 
    floor_handler.separate = floor_collide

    while True:
        #check to see if user wants to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]:
                    player.fly()
            if pressed[pygame.K_a]:
                player.steer(True)
            if pressed[pygame.K_d]:
                player.steer(False)
            if pressed[pygame.K_s]:
                player.brake()
        
        display.fill((255,255,255))#draw white background

        #draw objects
        player.draw()
        [ball.draw() for ball in balls]
        floor.draw()
        right_wall.draw()
        left_wall.draw()
        roof.draw()
        
        #tick sim
        tick += 1
        if tick>=ball_life:
            tick = 0
        elif tick%5 == 0:
            balls.append(Ball(random.randint(30,WITDH-30),HEIGHT+30, 2,(0,FORCE)))
        
        #Update display
        pygame.display.update()

        #FPS TICK
        clock.tick(FPS)
        space.step(1/FPS)

#RUN GAME
game()

pygame.quit()