import pygame as pg
import math

pg.init()

WINDOW_SIZE = (1280, 700)
SCREEN_SIZE = (640, 350)
COLORS = {
    "red" : (255, 0, 0),
    "blue" : (0, 0, 255),
    "green" : (0, 255, 0),
    "white" : (255, 255, 255),
    "black" : (0, 0, 0),
    "purple" : (48, 25, 52)
}

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    rotated_image.set_colorkey((0, 0, 0))

    surf.blit(rotated_image, new_rect)

class Player():
    def __init__(self, x, y, img):
        self.pos = [x, y]
        self.size = [16, 30]
        self.id = 0
        self.rotation = 0
        self.multi_collision = 0
        self.bullets = []
        self.bullets_stored_vel = [] 
        self.bullets_timer = []
        self.dead = 0
        self.restart = 0
        
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.pos[0] -= 3
            self.rotation += 1
        if keys[pg.K_d]:
            self.pos[0] += 3 
            self.rotation -= 1
        if keys[pg.K_w]:
            self.pos[1] -= 3 
        if keys[pg.K_s]:
            self.pos[1] += 3 

        i = 0
        while i < len(self.bullets):
            self.bullets[i].x += self.bullets_stored_vel[i][0]
            self.bullets[i].y += self.bullets_stored_vel[i][1]
            self.bullets_timer[i] += 1
            if self.bullets_timer[i] > (10 * 60):
                self.bullets.remove(self.bullets[i])
                self.bullets_stored_vel.remove(self.bullets_stored_vel[i])
                self.bullets_timer.remove(self.bullets_timer[i])
            i+= 1

        if abs(self.rotation) > 20:
            if self.rotation < 0:
                self.rotation = -20
            else: 
                self.rotation = 20

        if self.pos[1] > SCREEN_SIZE[1]:
            self.pos[1] = 0 + self.size[1]
        
        if self.pos[1] < 0:
            self.pos[1] = SCREEN_SIZE[1] - self.size[1]

        if self.pos[0] < 0:
            self.pos[0] = SCREEN_SIZE[0] - self.size[1]

        if self.pos[0] > SCREEN_SIZE[0]:
            self.pos[0] = 0 + self.size[0]

        if pg.mouse.get_pressed()[0]:
            m_pos = pg.mouse.get_pos() 
            distx = (m_pos[0] / 2) - self.pos[0]
            disty = (m_pos[1] / 2) - self.pos[1]
            angle = math.atan2(disty, distx)
            self.pos[0] -= math.cos(angle) * 5
            self.pos[1] -= math.sin(angle) * 5
            self.bullets.append(pg.Rect(self.pos, [10, 10]))
            self.bullets_stored_vel.append([math.cos(angle) * 10, math.sin(angle) * 10])
            self.bullets_timer.append(1)

        self.rect = pg.Rect(self.pos, self.size)
              
    def draw(self, screen, img):
        blitRotateCenter(screen, img, self.pos, self.rotation)
        for i in self.bullets:
            pg.draw.rect(screen, COLORS["red"], i)
        