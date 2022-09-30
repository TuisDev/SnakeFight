import socket
import sys
import pygame as pg
from pygame.locals import *
from servergame import Color, player_color
import threading
import time
import struct
port = 65432


def main(host, color):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        for i in color:
            s.send(struct.pack('>B',i))
        while s.recv(256)[:1] != b's': pass
        pg.init()
        print('HELLO')
        done = False
        screen = pg.display.set_mode((400, 400))

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        s.send(b'u')
                    elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                        s.send(b'r')
                    elif event.key == pg.K_DOWN or event.key == pg.K_s:
                        s.send(b'd')
                    elif event.key == pg.K_LEFT or event.key == pg.K_a:
                        s.send(b'l')
            pg.display.flip()
        pg.quit()

if __name__ == '__main__':
    main('127.0.0.1', Color.green)

            

