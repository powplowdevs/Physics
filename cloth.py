from numpy import mat
import pygame
import pymunk
from pymunk.body import Body
import time

#Start pygame
pygame.init()

#Make display
HEIGHT = 600
WITDH = 1000
display = pygame.display.set_mode((WITDH,HEIGHT))

#SET FPS
FPS = 50
clock = pygame.time.Clock()

#vars
matrix_x = 50
matrix_y = 50
buffer_sizeX = 10
buffer_sizeY = 10
start = (20,(buffer_sizeY*matrix_y)+20)
balls = []
strings = []
SIZE = 1


#our pymunk simulation "world" or space
space = pymunk.Space()
space.gravity = (0,-100)

#CONVERT PYGAME CORDS TO PYMUNK CORDS FUNCTION
def convert_cords(point):
    return point[0], WITDH-point[1]

class Ball(): 
    def __init__(self,x,y, vel, size=10,type=""):
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
        self.shape.density = 0.1
        self.shape.elasticity = 0
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
        self.joint = pymunk.PinJoint(self.body1,self.body2)
        space.add(self.joint)
    
    def draw(self):
        pos1 = convert_cords(self.body1.position)
        pos2 = convert_cords(self.body2.position)
        #draw joint
        pygame.draw.line(display, (0,0,0), pos1,pos2, 2)
    
    def cut(self, pos):
        if self.body1.position[1] - 20 < pos[1] and self.body2.position[1] + 20> pos[1]:
            if  self.body1.position[0] < pos[0] - 20 and self.body2.position[0] > pos[0] + 20 or self.body1.position[0] > pos[0] - 20 and self.body2.position[0] < pos[0] + 20:
                try:
                    space._remove_constraint(self.joint)
                    return pos, self.body1#, self.body1.body
                except:
                    return False
        return False

#GAME FUNCTION
def game():
    x,y = convert_cords(start)#(300,600))
    index = 0
    indexx = 0
    indexy = 0

    for i in range(matrix_y):
        y += buffer_sizeY
        x = start[0]
        for j in range(matrix_x):
            #if ((len(balls) + 1)/matrix_x) == matrix_x or (len(balls)/matrix_x) == matrix_x-1:
            #if i == (matrix_x-1) and j == 0 or i == (matrix_x-1) and j == matrix_x-1:
            if i == matrix_y-1 and j == 0 or i == matrix_y-1 and j == matrix_x-1:
                balls.append(Ball(x,y,(0,0),(SIZE),"s"))
            else:
                balls.append(Ball(x,y,(0,0),(SIZE)))
            x += buffer_sizeX
    
    for ball in balls:

        try:
            if indexx != matrix_x-1:
                strings.append(String(ball.body, balls[index+1].body))
        except:
            pass

        try:
            if indexy != matrix_y-1:
                strings.append(String(ball.body, balls[index+matrix_x].body))
        except:
            pass
    
        # try:
        #     strings.append(String(ball.body, balls[index+matrix_x].body))
        # except:
        #     pass

        # try:
        #     if index+1 != matrix_x and ".0" not in str((index+1)/matrix_x):
        #         strings.append(String(ball.body, balls[index+1].body))
        #         #print(f"ball{index} to ball{index+1} :: value_add {index+1} value_defult {index} :: div_val {((index+1)/matrix_x)}")
        # except:
        #     pass
        # try:
        #     strings.append(String(ball.body, balls[index+matrix_x].body))
        # except:
        #     pass

        index += 1
        indexx += 1
        if indexx == matrix_x:
            indexx = 0
            indexy += 1
        
    while True:
        #check to see if user wants to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


        display.fill((255,255,255))#draw white background

        mouse_pos = pygame.mouse.get_pos()

        #draw
        for ball in balls:
            ball.draw()
        for string in strings:
            string.draw()
            res = string.cut(convert_cords(mouse_pos))
            if res != False:
                strings.remove(string)
                #strings.append(String(res[1],convert_cords(mouse_pos), "position"))
                #pos = convert_cords(mouse_pos)
                #new_ball = Ball(pos[0],pos[1],(0,0),SIZE)
                #balls.append(new_ball)
                #strings.append(String(new_ball,res[2]))
     

        #Update display
        pygame.display.update()

        #FPS TICK
        clock.tick(FPS)
        space.step(1/FPS)

#RUN GAME
game()

pygame.quit()