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
from dataclasses import dataclass
import struct
from game import player_color
import time

snake_color_lst = [[]]
snake_num = 1
ready_snakes = 0b1


snake_color_lst[0].append(list(player_color.translate)[len(snake_color_lst[0])])

while True:
    data = b''
    body_len = len(snake_color_lst[0]) * 3
    hdr = struct.pack('>H', (snake_num << 4 | body_len) << 8 | ready_snakes)
    data += hdr
    for rgb in snake_color_lst:
            for color in rgb[0]:
                color_bin = struct.pack('>B', color)
                data += color_bin
    hdr = struct.unpack('>H', data[:2])[0]
    print(f'ready_snakes = {hdr & 0b11111111}')
    print(f'body_len = {hdr >> 8 & 0b1111}')
    print(f'snake_num = {hdr >> 12}')
    if input('Would you like to add another snake?(y/n): ') == 'y':
        snake_color_lst[0].append(list(player_color.translate)[len(snake_color_lst[0])])
    snake_num = int(input('What snake do you want to be?(int):  ')) - 1
    if ready_snakes & int(2**snake_num) == 0:
        if input('Is your snake ready?(y/n):  ') == 'y':
            ready_snakes = ready_snakes | int(2**snake_num)
    elif input('Are you still ready?(y/n):  ') == 'n':
        ready_snakes = ready_snakes ^  int(2**snake_num)
    
    if input('Would you like to ban a snake?(y/n):  ') == 'y':
        snake_color_lst[int(input('Which snake do you want to ban?(int):  ')) - 1] = (0, 0, 0)



    time.sleep(0.1)
