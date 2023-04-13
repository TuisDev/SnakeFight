# import pygame as pg
# from pygame.locals import *
# from game import Color, player_color

# pg.init()
# size = 500, 500
# width, height = size
# screen = pg.display.set_mode((size))
# clock = pg.time.Clock()
# font = pg.font.SysFont('Courier New', 16)
# done = False
# server_list = []
# activated_list = []

# reload = font.render('Refresh', True, Color.green, Color.blue)
# reload_size = reload.get_rect().size

# play = font.render('PLAY!', True, Color.grey_blue, Color.grey_green)
# play_size = play.get_rect().size

# list_box = Rect(70, 30, 360, 400)
# computer_list = ['bue', 'Jacob-Pc', 'Wesley-PC', 'Jacob Watson', 'McLean Muir', 'starwes654-PC', "I'm not high you're high", 'This is a scam']

# while not done:
#     for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True

#             if event.type == pg.MOUSEBUTTONDOWN:
#                 if width / 2 - (reload_size[0] + play_size[0] + 20) / 2 <= pg.mouse.get_pos()[0] <= width / 2 - play_size[0] / 2 - 20 + reload_size[0] / 2 and 450 <= pg.mouse.get_pos()[1] <= 450 + reload_size[1]:
#                     print('RELOAD')

#                 elif 70 <= pg.mouse.get_pos()[0] <= 430 and 30 <= pg.mouse.get_pos()[1] <= 430:
#                    if not int((pg.mouse.get_pos()[1] - 30) / 25) > len(server_list):
#                     if True in activated_list:
#                         activated_list[activated_list.index(True)] = False
#                     activated_list[int((pg.mouse.get_pos()[1] - 30) / 25)] = True

#                 elif width / 2 - play_size[0] / 2 + reload_size[0] / 2 + 10 <= pg.mouse.get_pos()[0] <= width / 2 + (reload_size[0] + play_size[0] + 20) / 2 and 450 <= pg.mouse.get_pos()[1] <= 450 + reload_size[1] and True in activated_list:
#                     print('PLAY!') 

#     if computer_list != []:
#         computer = computer_list[-1]
#         computer_list.pop(-1)

#         if len(computer) > 20:
#             computer = f'{computer[:20]}...'
#         white_space = ' ' * (23 - len(computer))
#         if not len(server_list) > 14:
#             server_list.append(f'{computer} {white_space} --- MAP')
#             activated_list.append(False)


#     screen.fill(Color.black)

#     for index, server in enumerate(server_list):
#         server_text = font.render(server, True, (Color.green, Color.blue)[index % 2])
#         server_rect = Rect(75, 35 + index * 25, 350, 25)
#         if activated_list[index]:
#             pg.draw.rect(screen, (Color.blue, Color.green)[index % 2], server_rect)
#         else:
#             pg.draw.rect(screen, (Color.blue, Color.green)[index % 2], server_rect, 3)
#         screen.blit(server_text, (server_rect.x + 5, server_rect.y + 5))

#     if True in activated_list:
#         play = font.render('PLAY!', True, Color.blue, Color.green)

#     pg.draw.rect(screen, Color.white, list_box, 5)
#     screen.blit(reload, (width / 2 - (reload_size[0] + play_size[0] + 20) / 2, 450))
#     screen.blit(play, (width / 2 - play_size[0] / 2 + reload_size[0] / 2 + 10, 450))
#     print(screen)
#     pg.display.update()

# pg.quit()





# import struct
# from game import player_color
# import time

# encoded = 0b010101011100110001100110.to_bytes(3, 'little')
# for byte in range(3):
#     for bit in range(0, 8, 2):
#         # print(bin((encoded[byte] << bit & 255) >> 6 - bit))
#         print(bit)
#         print(bin((0b10011001 << bit) & 0b11111111))
#         print(bin((0b10011001 << bit & 255) >> 6))

# print(int(bin(0b10101010)[:2:-1], 2))


## SENDING ARROW KEY TESTS ##

# import socket
# import sys
# from turtle import color
# import pygame as pg
# from pygame.locals import *
# from servergame import Color, player_color
# import threading
# import time
# import struct
# port = 65432
# color = []

# def connect(conn):
#     data_buffer = b''
#     data = conn.recv(4096)
#     data_buffer += data
#     for i in range(3):
#         color.append(struct.unpack('>B', data_buffer[:1])[0])
#     print(color)
#     conn.send(b's')
#     pg.init()
#     done = False
#     screen = pg.display.set_mode((400, 400))

#     while True:
#         data = conn.recv(256)
#         if data[:1] == b'u':
#             print('UP')
#         elif data[:1] == b'r':
#             print('LEFT')
#         elif data[:1] == b'd':
#             print('DOWN')
#         elif data[:1] == b'l':
#             print('RIGHT')

#     pg.display.flip()
#     pg.quit()

# def main(host):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((host, port))
#         s.listen(7)
#         conn, addr = s.accept()
#         threading.Thread(target=connect, args=(conn,)).start()
       

# if __name__ == '__main__':
#     main('127.0.0.1')





### SENDING DATA FROM SERVER GAME TO CLIENT GAME ###

import socket
import struct
from servergame import Snake
from servergame import player_color

ipv4_host = '127.0.0.1'
ipv4_port = 65432

 
husk = [[118, 120, 20, 20], [120, 120, 20, 20], [120, 118, 20, 20], [120, 116, 20, 20], [120, 114, 20, 20], [120, 112, 20, 20], [120, 110, 20, 20], [120, 108, 20, 20]]

green_snake = Snake('south', (0, 0, 0, 0), player_color.green, 20, (80, 80))
green_snake.degree = 180
yellow_snake = Snake('south', (0, 0, 0, 0), player_color.yellow, 20, (20, 20))
yellow_snake.degree = 90
red_snake = Snake('south', (0, 0, 0, 0), player_color.red, 20, (40, 40))
red_snake.offset = [0, red_snake.size]
blue_snake = Snake('south', (0, 0, 0, 0), player_color.blue, 20, (40, 60))
blue_snake.offset = [blue_snake.size, 0]
blue_snake.attack = True
snakes = [green_snake, blue_snake, red_snake, yellow_snake]



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        with open('map.txt', 'rb') as map_file:
            map_info = map_file.readline()

        print(f'THIS {(ipv4_host, ipv4_port)}')
        s.bind((ipv4_host, ipv4_port))
        s.listen(20)
        conn, addr = s.accept()
        done = False
        while True:
            # Send Map
            data = struct.pack('>B', len(map_info))
            conn.send(data)
            conn.sendall(map_info)

            # Send snakes
            data = struct.pack('>B', len(snakes))
            conn.send(data)
            for snake in snakes:
                data = struct.pack('>B', (snake.attack << 7) | (snake.size << 2) | (int)(snake.degree / 90))
                conn.send(data)

                data = struct.pack('>h', snake.head.x)
                conn.sendall(data)
                data = struct.pack('>h', snake.head.y)
                conn.sendall(data)

                data = struct.pack('>h', len(snake.pos_lst) * 4)
                conn.sendall(data)

                for pos in snake.pos_lst:
                    conn.sendall(struct.pack('>h', int(pos[0] / 2)))
                    conn.sendall(struct.pack('>h', int(pos[1] / 2)))

            # Send husks
            data = struct.pack('>h', len(husk)*4)
            conn.sendall(data)
            for block in husk:
                conn.sendall(struct.pack('>h', int(block[0] / 2)))
                conn.sendall(struct.pack('>h', int(block[1] / 2)))
    except KeyboardInterrupt:
        print('BYEBYEBYE')