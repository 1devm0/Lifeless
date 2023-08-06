import sys
import pygame as pg
from framework import *
from network import * 
import random

pg.init()

window = pg.display.set_mode(WINDOW_SIZE)
pg.display.set_caption("Lifeless")

screen = pg.Surface(SCREEN_SIZE)

running = 1

n = None

player = Player(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2, "res/robot.png")
p2 = Player(0, 100, "res/robot_two.png")
clock = pg.time.Clock()

font = pg.font.Font("res/m6x11.ttf", 25)
font_two = pg.font.Font("res/m6x11.ttf", 25)
curr_font = 0
special = [font, font_two]
curr_color = 0
colors = ["white", "red", "purple", "blue", "green"]

menu = 1
singleplayer = 0
multiplayer = 0


single_font = font.render("Play Single Player", True, COLORS["white"])
multi_font = font.render("Play Multi Player", True, COLORS["white"])

sf_size = single_font.get_size()
sf_rect = pg.Rect(SCREEN_SIZE[0] / 2 - sf_size[0] / 2, 
                SCREEN_SIZE[1] / 2, sf_size[0], sf_size[1])

mf_size = multi_font.get_size()
mf_rect = pg.Rect(SCREEN_SIZE[0] / 2 - mf_size[0] / 2, 
                SCREEN_SIZE[1] / 2 + 100, mf_size[0], mf_size[1])

enemies = []
gen_en = 0
paused_position_rec = 0
pause_time = 0
survived = 0
alive = 1
enemies_killed = 0
enemy_speeds = []

scroll = []

# add some screen shake
# particles
# sound effects
once = 0

imgs = {
    "1" : pg.transform.scale(pg.image.load("res/robot.png").convert(), (16, 30)),
    "2" : pg.transform.scale(pg.image.load("res/robot_two.png").convert(), (16, 30))
} 
imgs["1"].set_colorkey((0, 0, 0))
imgs["2"].set_colorkey((0, 0, 0))

particles = []

explosion_sound = pg.mixer.Sound("res/explosion.wav")
projectile_sound = pg.mixer.Sound("res/projectile.wav")

while running: 
    while menu:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                menu = 0
                running = 0

        if pg.mouse.get_pressed()[0]:
            m_posx = pg.mouse.get_pos()[0] / 2
            m_posy = pg.mouse.get_pos()[1] / 2 

            m_rect = pg.Rect(m_posx, m_posy, 10, 10) 
            if m_rect.colliderect(sf_rect):
                menu = 0
                singleplayer = 1
            if m_rect.colliderect(mf_rect):
                menu = 0
                multiplayer = 1

        screen.fill(COLORS["purple"])

        screen.blit(single_font, sf_rect)
        screen.blit(multi_font, mf_rect)

        pg.transform.scale(screen, WINDOW_SIZE, window)
        pg.display.update()
        clock.tick(60)


    while singleplayer:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                singleplayer = 0
                running = 0
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    singleplayer = 0
                    menu = 1

        if alive: 
            player.update()
            # p2.update()
            gen_en += 1

            if gen_en % (0.25 * 60) == 0:
                stored_position = player.pos

            if gen_en % (0.5 * 60) == 0:
                enemies.append(pg.Rect(random.randint(0 - 200, 0),
                                    random.randint(0, SCREEN_SIZE[1]), 
                                    20, 20))
                enemies.append(pg.Rect(random.randint(SCREEN_SIZE[0], SCREEN_SIZE[0] + 200),
                                    random.randint(0, SCREEN_SIZE[1]), 
                                    20, 20))
                enemy_speeds.append([random.randint(1, 3), random.randint(1, 3)])
                enemy_speeds.append([random.randint(1, 3), random.randint(1, 3)])
                gen_en = 0

            n = 0
            for i in enemies:
                distx = stored_position[0] - i.x
                disty = stored_position[1] - i.y 
                angle = math.atan2(disty, distx)
                i.x += math.cos(angle) * enemy_speeds[n][0] 
                i.y += math.sin(angle) * enemy_speeds[n][1] 
                n +=1
                if i.colliderect(player.rect):
                    alive = 0
                for x in player.bullets:
                    if x.colliderect(i):
                        try:
                            for m in range(10, 50):
                                particles.append([[i.x, i.y], [random.randint(-5, 5), random.randint(-5, 5)], random.randint(2, 9)])
                            explosion_sound.play()
                            enemies.remove(i)
                            player.bullets.remove(x)
                        except Exception as e:
                            pass
                        enemies_killed += 1

            screen.fill(COLORS["purple"])


            player.draw(screen, imgs["1"])

            survived += 1
            time = font.render("Survived for " + str(int(survived / 60)) + " seconds", True, COLORS["white"])
            kills = special[random.randint(0, 1)].render("Kills: " + str(enemies_killed), True, COLORS[colors[random.randint(0, len(colors) - 1)]])
            screen.blit(time, (SCREEN_SIZE[0] / 2 - time.get_size()[0] / 2, 10))
            screen.blit(kills, (SCREEN_SIZE[0] / 2 - kills.get_size()[0] / 2, 30))

            if len(particles) > 0:
                for p in particles:
                    p[0][0] += p[1][0]
                    p[0][1] += p[1][1]
                    p[2] -= 0.1
                    pg.draw.circle(screen, COLORS[colors[random.randint(0, len(colors) - 1)]], p[0], p[2])
                    if p[2] <= 0:
                        try:
                            p.remove(p)
                        except Exception as e:
                            pass


            for i in enemies:
                screen.blit(imgs["2"], i)

        else:
            screen.fill(COLORS["black"])
            time = font.render("Survived for " + str(int(survived / 60)) + " seconds", True, COLORS["white"])
            kills = font.render("Kills: " + str(enemies_killed), True, COLORS["white"])

            play_again  = font.render("Play again by pressing R", True, COLORS["white"])

            screen.blit(time, (SCREEN_SIZE[0] / 2 - time.get_size()[0] / 2, 10))
            screen.blit(kills, (SCREEN_SIZE[0] / 2 - kills.get_size()[0] / 2, 30))
            screen.blit(play_again, (SCREEN_SIZE[0] / 2 - play_again.get_size()[0] / 2, SCREEN_SIZE[1] / 2 - play_again.get_size()[1] / 2))
            keys = pg.key.get_pressed()
            player.bullets = []
            enemies = []
            player.pos = [SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2]
            enemy_speeds = []
            if keys[pg.K_r]:
                survived = 0
                enemies_killed = 0
                alive = 1

        pg.transform.scale(screen, WINDOW_SIZE, window)
        pg.display.update()
        clock.tick(60)



    while multiplayer:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                multiplayer = 0
                running = 0
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    multiplayer = 0
                    menu = 1


        if alive == 1:
            if not once:
                n = Network()
                # start_position = read_position(n.get_pos())
                player = n.get_p()
                once = 1
            # p2_pos = read_position(n.send(make_pos_str((player.pos[0], player.pos[1]))))
            if p2 != None:
                for i in p2.bullets:
                    if player.rect.colliderect(i):
                        player.dead = 1
                    pg.draw.rect(screen, COLORS["white"], i)
            
            player.update()
            p2 = n.send(player) 
            if p2 != None: 
                if p2.dead:
                    alive = 3

            if player.dead:
                alive = 0
            
            screen.fill(COLORS["purple"])

            player.draw(screen, imgs["1"])
            if p2 != None:
                p2.draw(screen, imgs["2"])

            time = font.render("Survived for " + str(int(pg.time.get_ticks() / 1000)) + " seconds", True, COLORS["white"])
            screen.blit(time, (SCREEN_SIZE[0] / 2 - time.get_size()[0] / 2, 10))
        if alive == 0: 
            screen.fill(COLORS["black"])
            time = font.render("Died", True, COLORS["white"])
            play_again  = font.render("Play again by pressing R", True, COLORS["white"])

            screen.blit(time, (SCREEN_SIZE[0] / 2 - time.get_size()[0] / 2, 10))
            screen.blit(play_again, (SCREEN_SIZE[0] / 2 - play_again.get_size()[0] / 2, SCREEN_SIZE[1] / 2 - play_again.get_size()[1] / 2))

            keys = pg.key.get_pressed()
            player.bullets = []
            enemies = []
            player.pos = [SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2]
            enemy_speeds = []
            once = 0
            if keys[pg.K_r]:
                survived = 0
                enemies_killed = 0
                alive = 1
                player.dead = 0
                p2 = None

        if alive == 3:
            screen.fill(COLORS["black"])
            time = font.render("YOU WON", True, COLORS["white"])
            play_again  = font.render("Play again by pressing R", True, COLORS["white"])

            screen.blit(time, (SCREEN_SIZE[0] / 2 - time.get_size()[0] / 2, 10))
            screen.blit(play_again, (SCREEN_SIZE[0] / 2 - play_again.get_size()[0] / 2, SCREEN_SIZE[1] / 2 - play_again.get_size()[1] / 2))

            keys = pg.key.get_pressed()
            player.bullets = []
            enemies = []
            player.pos = [SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2]
            enemy_speeds = []
            if keys[pg.K_r]:
                survived = 0
                enemies_killed = 0
                alive = 1
                player.dead = 0
                p2 = None

        pg.transform.scale(screen, WINDOW_SIZE, window)
        pg.display.update()
        clock.tick(60)


sys.exit()
