'''
THIS IS THE TITLE SCREEN
NOT THE GAME
'''

import sys
import pygame as pg
from pygame.locals import *
import random
import os
from game import Color

pg.init()
size = 500, 500
width, height = size
screen = pg.display.set_mode((size))
clock = pg.time.Clock()
font = pg.font.Font('freesansbold.ttf', 32)
done = False

start = font.render(' Snake Fight! ', True, Color.green, Color.blue)
start_size = start.get_rect().size

join = font.render('  Join  ', True, Color.blue, Color.green)
join_size = join.get_rect().size

host = font.render('  Host  ', True, Color.blue, Color.green)
host_size = host.get_rect().size

while not done:
    screen.blit(start, (width / 2 - start_size[0] / 2, 325))
    screen.blit(join, (width / 2 - join_size[0] - 7, 365))
    screen.blit(host, (width / 2 + host_size[0] - 105, 365))
    title_pic = pg.image.load('logo.png')
    title_pic = pg.transform.scale(title_pic, (390, 200))
    title_rect = title_pic.get_rect().size
    screen.blit(title_pic, (55, 100))
 
    for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if width / 2 - join_size[0] - 7 <= pg.mouse.get_pos()[0] <= width / 2 - 7  and 365 <= pg.mouse.get_pos()[1] <= 365 + join_size[1]:
                    pg.display.quit()
                    os.system('python client.py')
                elif width / 2 + host_size[0] - 105 <= pg.mouse.get_pos()[0] <= width / 2 + 105 and 365 <= pg.mouse.get_pos()[1] <= 365 + host_size[1]:
                    pg.display.quit()
                    os.system('python server.py')
               
    pg.display.flip()
    clock.tick(100)