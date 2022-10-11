#### SEND DATA TO SERVER CODE ####



# import socket
# import sys
# import pygame as pg
# from pygame.locals import *
# from servergame import Color, player_color
# import threading
# import time
# import struct
# port = 65432


# def main(host, color):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((host, port))
#         for i in color:
#             s.send(struct.pack('>B',i))
#         while s.recv(256)[:1] != b's': pass
#         pg.init()
#         print('HELLO')
#         done = False
#         screen = pg.display.set_mode((400, 400))

#         while not done:
#             for event in pg.event.get():
#                 if event.type == pg.QUIT:
#                     done = True
#                 elif event.type == pg.KEYDOWN:
#                     if event.key == pg.K_UP or event.key == pg.K_w:
#                         s.send(b'u')
#                     elif event.key == pg.K_RIGHT or event.key == pg.K_d:
#                         s.send(b'r')
#                     elif event.key == pg.K_DOWN or event.key == pg.K_s:
#                         s.send(b'd')
#                     elif event.key == pg.K_LEFT or event.key == pg.K_a:
#                         s.send(b'l')
#             pg.display.flip()
#         pg.quit()

# if __name__ == '__main__':
#     main('127.0.0.1', Color.green)

            

#### RECIEVE DATA FROM SERVER CODE ####

import pygame as pg
from pygame.locals import *
from servergame import Color, player_color
import socket
import struct
from servergame import Color, player_color

## Initial input variables
host = '127.0.0.1'
color = Color.green

# LOCAL VARIABLES #

port = 65432

total_width, total_height = 700, 700
total_screen = pg.Surface((700, 700))

width, height = 500, 500
screen = pg.Surface((500, 500))

fang_bite = [
        pg.image.load('fang1.png'), pg.image.load('fang2.png'),
        pg.image.load('fang3.png'), pg.image.load('fang4.png'),
        pg.image.load('fang4.png'), pg.image.load('fang4.png'),
        pg.image.load('fang4.png'), pg.image.load('fang4.png'),
        pg.image.load('fang3.png'), pg.image.load('fang2.png'), 
    ]


# requried variabels to be sent

def main(host, color):
    snakes = None
    husk = None
    map_file = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        pg.init()
        done = False
        screen = pg.display.set_mode((400, 400))


        while not done:
            data += s.recv(4096)
            if len(data) >= 2:
                pass

            with open('map.txt', 'rb') as map_file:
                    map_info = map_file.readline()


            ## Drawing Code ##

            if len(snakes) > 1:
                        screen.fill(Color.grey)

                        for i in range(625):
                            color_alternate = {0: (174, 247, 119), 1:(134, 189, 92)}
                            pg.draw.rect(screen, color_alternate[(i % 25 + int(i / 25)) % 2], ((i % 25) * 20, int(i / 25) * 20, 20, 20))

                        for snake in snakes:
                            if snake.attack:
                                print(snake.animation_tick)
                                if snake.animation_tick > len(fang_bite) - 1:
                                    snake.animation_tick = -1
                                    snake.attack = False
                                if snake.degree == 270 or snake.degree == 0:
                                    snake.offset = 0, 0
                                elif snake.degree == 90:
                                    snake.offset = 0, snake.size
                                else:
                                    snake.offset = snake.size, 0
                                screen.blit(pg.transform.rotate(fang_bite[snake.animation_tick], snake.degree), (snake.head.x - snake.offset[0], snake.head.y - snake.offset[1]))
                                snake.animation_tick += 1
                        
                        for rect in husk:
                            pg.draw.rect(screen, Color.purple, Rect(rect))    
                            

                        for i in range(625):
                            byte = int(i / 4)
                            bit = 2 * (i % 4)
                            binary_to_image = {0b01: 'brick.png', 0b10: 'wood.png', 0b11: 'apple.png', 0b00: 'blank'}
                            image = binary_to_image[(map_info[byte] << bit & 255) >> 6]
                            if image != 'blank':
                                image = pg.image.load(image)
                                image = pg.transform.scale(image, (20, 20))
                                screen.blit(image, ((i % 25) * 20, int(i / 25) * 20))



                        for snake in snakes:
                            for rect in snake.pos_lst:
                                pg.draw.rect(screen, snake.color, rect)                                                                                   
                            # pg.draw.rect(screen, Color.red, snake.face, 1)
                            # pg.draw.rect(screen, Color.green, snake.fangs, 1)
                            
            else:
                        print(snakes[0].color)
                        return snakes[0].color
                    
                    
            total_screen.blit(screen, (100, 100))

            snake_num = [snake.color for snake in snakes].index(Color.green)


            sub = total_screen.subsurface((snakes[snake_num].head.x, snakes[snake_num].head.y, 200, 200)).copy()
            sub = pg.transform.scale(sub, (400, 400))
            snake_window = pg.display.set_mode((400, 400))
            pg.display.set_caption(player_color.translate[snakes[snake_num].color])
            snake_window.blit(sub, (0, 0))

if __name__ == '__main__':
    main(host, color)