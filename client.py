
import socket
import sys
import pygame as pg
from pygame.locals import *
from game import Color, player_color
import threading
import time
import struct

computer_name = socket.gethostname()
ipv6_multicast = "ff02::face:1"
ipv6_port = 65431
ipv4_host = ''
ipv4_port = 65432
start_time = time.time()
received = [None]
thread_pool = [0]
data_buffer = b''
socket.setdefaulttimeout(5)

def check_group(udp_sock):
    try:
        udp_sock.sendto("I want to play snake".encode(), (ipv6_multicast, ipv6_port))
        received[0] = udp_sock.recvfrom(1024)
    except OSError or TimeoutError:
        pass
    finally:
        thread_pool[0] -= 1


def color_picker():
    pass

def server_finder():
    size = 500, 500
    width, height = size
    screen = pg.display.set_mode((size))
    font = pg.font.SysFont('Courier New', 16)
    done = False
    server_list = []
    activated_list = []

    reload = font.render('Refresh', True, Color.green, Color.blue)
    reload_size = reload.get_rect().size

    play = font.render('PLAY!', True, Color.grey_blue, Color.grey_green)
    play_size = play.get_rect().size

    list_box = Rect(70, 30, 360, 400)
    addr_lst = list()
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.settimeout(1)
        while not done:
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if width / 2 - (reload_size[0] + play_size[0] + 20) / 2 <= pg.mouse.get_pos()[0] <= width / 2 - play_size[0] / 2 - 20 + reload_size[0] / 2 and 450 <= pg.mouse.get_pos()[1] <= 450 + reload_size[1]:
                            pg.display.quit()
                            return False

                        elif 70 <= pg.mouse.get_pos()[0] <= 430 and 30 <= pg.mouse.get_pos()[1] <= 430:
                            if not int((pg.mouse.get_pos()[1] - 30) / 25) > len(server_list) - 1:
                                if True in activated_list:
                                    activated_list[activated_list.index(True)] = False
                                activated_list[int((pg.mouse.get_pos()[1] - 30) / 25)] = True

                        elif width / 2 - play_size[0] / 2 + reload_size[0] / 2 + 10 <= pg.mouse.get_pos()[0] <= width / 2 + (reload_size[0] + play_size[0] + 20) / 2 and 450 <= pg.mouse.get_pos()[1] <= 450 + reload_size[1] and True in activated_list:
                            return ipv4_host

            if thread_pool[0] < 1:
                thread_pool[0] += 1
                threading.Thread(target=check_group, args=(udp_sock,), daemon=True).start()

            if received[0] is not None:
                data = received[0][0].decode()
                addr = received[0][1]
                server_name, ipv4_host = data.split(', ')

            if received[0] is not None and addr not in addr_lst:
                addr_lst.append(addr)

                if len(server_name) > 20:
                    server_name = f'{server_name[:20]}...'
                white_space = ' ' * (23 - len(server_name))
                if not len(server_list) > 14:
                    server_list.append(f'{server_name} {white_space} --- MAP')
                    activated_list.append(False)


            screen.fill(Color.black)

            for index, server in enumerate(server_list):
                server_text = font.render(server, True, (Color.green, Color.blue)[index % 2])
                server_rect = Rect(75, 35 + index * 25, 350, 25)
                if activated_list[index]:
                    pg.draw.rect(screen, (Color.blue, Color.green)[index % 2], server_rect)
                else:
                    pg.draw.rect(screen, (Color.blue, Color.green)[index % 2], server_rect, 3)
                screen.blit(server_text, (server_rect.x + 5, server_rect.y + 5))

            if True in activated_list:
                play = font.render('PLAY!', True, Color.blue, Color.green)

            pg.draw.rect(screen, Color.white, list_box, 5)
            screen.blit(reload, (width / 2 - (reload_size[0] + play_size[0] + 20) / 2, 450))
            screen.blit(play, (width / 2 - play_size[0] / 2 + reload_size[0] / 2 + 10, 450))
            pg.display.update()
        
        return 'QUIT'

if __name__ == '__main__':
    pg.init()
    ipv4_host = server_finder()
    while not ipv4_host: ipv4_host = server_finder()
    pg.quit()
    if ipv4_host == 'QUIT':
        sys.exit()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print((ipv4_host, ipv4_port))
        s.connect((ipv4_host, ipv4_port))
        snake_color_lst = []
        pg.init()
        done = False
        size = 500, 500
        width, height = size
        screen = pg.display.set_mode((size))
        clock = pg.time.Clock()
        font = pg.font.Font('freesansbold.ttf', 32)
        ready = False

        lobby = font.render(' Lobby ', True, Color.green, Color.blue)
        lobby_size = lobby.get_rect().size

        ready_txt = font.render(' Ready ', True, Color.blue, Color.green)
        ready_size = lobby.get_rect().size


        rect = Rect(width / 2 - 400 / 2, 90, 400, 300)
        s.sendall(b'Hello')
        while not done:
            data = s.recv(4096)
            if data:
                data_buffer += data
            if len(data_buffer) >= 2:
                hdr = struct.unpack('>H', data_buffer[:2])[0]
                body_len = hdr >> 8 & 0b1111
                ready_snakes = hdr & 0xff
            if len(data_buffer) >= body_len + 2:
                data_buffer = data_buffer[2:]
                snake_color_lst = []
                for i in range(int(body_len / 3)):
                    color = []
                    for i in range(3):
                        color.append(struct.unpack('>B', data_buffer[:1])[0])
                        data_buffer = data_buffer[1:]
                    snake_color_lst.append(tuple(color))

            screen.fill(Color.black)
            snk_num = len(snake_color_lst)
            screen.blit(lobby, (width / 2 - lobby_size[0] / 2, 10))
            screen.blit(ready_txt, (width / 2 - ready_size[0] / 2, 400))

            pg.draw.rect(screen, Color.white, rect, 1)
            snk = Rect(width / 2 - (snk_num * 25 + (snk_num - 1) * 25) / 2, 250, 25, 140)
           
            for i in range(snk_num):
                if (ready_snakes << i & 0xff) >> 7 == 1:
                    snk.y = 175
                    snk.size = (snk.size[0], 215)
                else:
                    snk.y = 250
                    snk.size = (snk.size[0], 140)
                    
                pg.draw.rect(screen, snake_color_lst[i], snk)
                
                snk.x += 50

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    if width / 2 - ready_size[0] <= pg.mouse.get_pos()[0] <= width / 2 and 400 <= pg.mouse.get_pos()[1] <= 400 + ready_size[1]:
                        ready = True
            if ready:
                s.sendall(b'f')
            else:
                s.sendall(b'g')

            pg.display.flip()
            clock.tick(100) 
        pg.quit()
        sys.exit()