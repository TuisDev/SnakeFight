'''
THIS IS THE TITLE SCREEN
NOT THE GAME
'''

import sys
import pygame as pg
from pygame.locals import *
import random
import os
from servergame import Color

pg.init()
screen = pg.display.set_mode((500, 500), pg.RESIZABLE)
clock = pg.time.Clock()
done = False

while not done:
    size = screen.get_size()
    if size[0] < size[1]:
        length = size[0]
    else:
        length = size[1]
    vl = length / 100
    offsetx = int((size[0] - length) / 2)
    offsety = int((size[1] - length) / 2)

    font = pg.font.Font('freesansbold.ttf', int(6.4 * vl))

    start = font.render(' Snake Fight! ', True, Color.green, Color.blue)
    start_size = start.get_rect().size

    join = font.render('  Join  ', True, Color.blue, Color.green)
    join_size = join.get_rect().size

    host = font.render('  Host  ', True, Color.blue, Color.green)
    host_size = host.get_rect().size

    screen.blit(start, (offsetx + length / 2 - start_size[0] / 2, offsety + int(65 * vl))) 
    screen.blit(join, (offsetx + length / 2 - join_size[0] - int(1.4 * vl), offsety + int(73 * vl))) 
    screen.blit(host, (offsetx + length / 2 + host_size[0] - int(21 * vl), offsety + int(73 * vl)))
    title_pic = pg.image.load('logo.png')
    title_pic = pg.transform.scale(title_pic, (int(78 * vl), int(40 * vl)))
    title_rect = title_pic.get_rect().size
    screen.blit(title_pic, (offsetx + int(11 * vl), offsety + int(20 * vl)))
 
    for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if offsetx + length / 2 - join_size[0] - int(1.4 * vl) <= pg.mouse.get_pos()[0] <= offsetx + length / 2 - int(1.4 * vl)  and offsety + int(73 * vl) <= pg.mouse.get_pos()[1] <= offsety + int(73 * vl) + join_size[1]:
                    pg.display.quit()
                    os.system('python client.py')
                elif offsetx + length / 2 + host_size[0] - int(21 * vl + offsetx) <= pg.mouse.get_pos()[0] <= offsetx + length / 2 + int(21 * vl) and offsety + int(73 * vl) <= pg.mouse.get_pos()[1] <= offsety + int(73 * vl) + host_size[1]:
                    pg.display.quit()
                    os.system('python server.py')
               
    pg.display.flip()
    clock.tick(100)