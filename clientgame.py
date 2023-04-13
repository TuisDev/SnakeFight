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
from servergame import Color, player_color, Snake
import socket
import struct


## Initial input variables
host = '127.0.0.1'
color = Color.green
color_lst = [player_color.green, player_color.blue, player_color.red, player_color.yellow]

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

def main(host, color, color_lst):
    snakes = []
#.attack (1 bit, fixed)
#.animation_tick (4 bit; fixed; +1 for transit) ## NOPE
#.degree (2 bit; fixed; / 90 for transit)
#.offset (2 bit; fixed; / size for transit) ## NOPE
#.size (5 bit; fixed for now)
#.pos_list ()
#.head.x
#.head.y
    map_info = None






    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((host, port))
        pg.init()
        done = False
        data_buffer = b''
        husk = []
        husk_len = 10
        screen = pg.display.set_mode((400, 400))
        with open('map.txt', 'rb') as map_file:
            map_info = map_file.readline()

        while not done:
            while True:
                data = s.recv(4096)
                if data:
                    data_buffer += data

                if len(data_buffer) >= 1:
                    map_len = struct.unpack('>B', data_buffer[:1])[0]
                if len(data_buffer) >= map_len + 1:
                    map_info = data_buffer[1:map_len+1]
                if len(data_buffer) >= map_len + 2:
                    snake_num = struct.unpack('>B', data_buffer[map_len + 1: map_len + 2])[0]
                if len(data_buffer) >= map_len + 2 + 7 * snake_num:
                    pos_lst_len = []
                    for i, snake_color in enumerate(color_lst):
                        snake_info = struct.unpack('>B', data_buffer[map_len + 2 + 7 * i: map_len + 3 + 7 * i])[0]
                        size = (snake_info >> 2) & 0b11111
                        snakes.append(Snake('',(0, 0, 0, 0), snake_color, size, (0, 0)))
                        snakes[i].attack = snake_info >> 7
                        snakes[i].degree = (snake_info & 0b11) * 90

                        headx = struct.unpack('>h', data_buffer[map_len + 3 + 7 * i: map_len + 5 + 7 * i])[0]
                        heady = struct.unpack('>h', data_buffer[map_len + 5 + 7 * i: map_len + 7 + 7 * i])[0]
                        snakes[i].head = Rect(headx, heady, size, size)
                        
                        pos_lst_len.append(struct.unpack('>h', data_buffer[map_len + 7 + 7 * i: map_len + 9 + 7 * i])[0])
                    
                    pos_lst_total_len = 0
                    for length in  pos_lst_len:
                        pos_lst_total_len += length

                
                if len(data_buffer) >= map_len + 2 + 7 * snake_num + pos_lst_total_len:
                    for j, snake in enumerate(snakes):
                        pos_lst = []
                        print(pos_lst_len[j] / 4)
                        for i in range(int(pos_lst_len[j] / 4)):
                            x = struct.unpack('>h', data_buffer[map_len + 9 + 4 * i + pos_lst_len[j]: map_len + 11 + 4 * i + pos_lst_len[j]])[0]
                            y = struct.unpack('>h', data_buffer[map_len + 11 + 4 * i + pos_lst_len[j]: map_len + 13 + 4 * i + pos_lst_len[j]])[0]
                            pos_lst.append([x, y, snake.size, snake.size])
                        snake.pos_lst = pos_lst
                if len(data_buffer) >= map_len + 4 + 7 * snake_num + pos_lst_total_len:
                    husk_len = struct.unpack('>h', data_buffer[1 + map_len: 1 + map_len + 2])[0]
                if len(data_buffer) >= map_len + 4 + 7 * snake_num + pos_lst_total_len + husk_len:
                    husk = []
                    for i in range(int(husk_len / 4)):
                        x = struct.unpack('>h', data_buffer[map_len + 3 + 7 * snake_num + i*4 + pos_lst_total_len: map_len + 5 + 7 * snake_num + i*4])[0] * 2
                        y = struct.unpack('>h', data_buffer[map_len + 5 + 7 * snake_num + i*4 + pos_lst_total_len: map_len + 7 + 7 * snake_num + i*4])[0] * 2
                        husk.append([x, y, snakes[0].size, snakes[0].size])
                    data_buffer = data_buffer[husk_len + 3 + 7 * snake_num + pos_lst_total_len + map_len:]

                


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

            snake_num = [snake.color for snake in snakes].index(color)


            sub = total_screen.subsurface((snakes[snake_num].head.x, snakes[snake_num].head.y, 200, 200)).copy()
            sub = pg.transform.scale(sub, (400, 400))
            snake_window = pg.display.set_mode((400, 400))
            pg.display.set_caption(player_color.translate[snakes[snake_num].color])
            snake_window.blit(sub, (0, 0))

if __name__ == '__main__':
    main(host, color, color_lst)