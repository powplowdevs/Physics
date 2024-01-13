import pygame
import pymunk
from pymunk.body import Body
import random, colorsys

# Start pygame
pygame.init()

# Make display
HEIGHT = 700
WIDTH = 800
display = pygame.display.set_mode((WIDTH, HEIGHT))

# Set FPS
FPS = 50
clock = pygame.time.Clock()

# Create pymunk spacecon
space = pymunk.Space()
space.gravity = (0, -1000)
# Dead handler
def null_collision_handler(arbiter, space, data):
    return False
pymunk.collision_handler = null_collision_handler

# Convert pygame coordinates to pymunk coordinates function
def convert_coords(point):
    return point[0], WIDTH - point[1]

class Ball(): 
    def __init__(self, x, y, vel, size=0.1, type=""):
        self.size = size
        if type == "s":
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body()
        self.body.position = x, y
        self.body.velocity = vel
        self.shape = pymunk.Circle(self.body, size)
        self.shape.density = 999999999
        self.shape.elasticity = 0
        #self.shape.filter = pymunk.ShapeFilter(group=1)
        space.add(self.body, self.shape)
    
    def draw(self):
        x, y = convert_coords(self.body.position)
        pygame.draw.circle(display, (0, 0, 0), (int(x), int(y)), self.size)

class String():
    def __init__(self, body1, attachment, color, identifier="body"):
        self.body1 = body1
        self.color = color
        if identifier == "body":
            self.body2 = attachment
        elif identifier == "position":
            self.body2 = pymunk.Body(body_type=Body.STATIC)
            self.body2.position = attachment
        joint = pymunk.PinJoint(self.body1, self.body2)
        space.add(joint)
    
    def draw(self):
        pos1 = convert_coords(self.body1.position)
        pos2 = convert_coords(self.body2.position)
        pygame.draw.line(display, self.color, pos1, pos2, 1)

def generate_rainbow_colors(num_colors):
    colors = []
    hue_range = 360 / num_colors

    for i in range(num_colors):
        hue = i * hue_range
        rgb = colorsys.hsv_to_rgb(hue / 360, 1, 1)
        colors.append((int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)))

    return colors




#GAME FUNCTION
def game():

    amt = 500
    ran = False

    balls = []
    strings = []
    colors = generate_rainbow_colors(amt)
    collision_group = 1

    count = 1

    for i in range(amt):
        if not ran:
            balls.append(Ball(300, 500, (0, 0)))
            balls[-1].shape.filter = pymunk.ShapeFilter(group=collision_group)
            collision_group+=1
            balls.append(Ball(340, 550, (0, 700)))
            balls[-1].shape.filter = pymunk.ShapeFilter(group=collision_group)
            collision_group+=1
            strings.append(String(balls[2*i].body, (400, 550), colors[i], "position"))
            strings.append(String(balls[2*i].body, balls[2*i+1].body, colors[i]))
        else:
            balls.append(Ball(random.uniform(290, 310), random.uniform(490,510), (0, 0)))
            balls[-1].shape.filter = pymunk.ShapeFilter(group=collision_group)
            collision_group+=1
            balls.append(Ball(random.uniform(170,180), random.uniform(490,510), (0, random.uniform(890,910))))
            balls[-1].shape.filter = pymunk.ShapeFilter(group=collision_group)
            collision_group+=1
            strings.append(String(balls[2*i].body, (400, 550), colors[i], "position"))
            strings.append(String(balls[2*i].body, balls[2*i+1].body, colors[i]))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        display.fill((0, 0, 0))

        for s in strings:
            s.draw()
        # n = random.randrange(0,5)
        # for b in balls:
        #     b.body.velocity = (b.body.velocity[0], b.body.velocity[1] + n)

        pygame.display.update()
        clock.tick(FPS)
        space.step(1 / FPS)

#RUN GAME
game()

pygame.quit()