65432
import socket
import sys
import pygame as pg
from pygame.locals import *
from servergame import Color, player_color
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
is_ready = False
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
    screen = pg.display.set_mode((500, 500), pg.RESIZABLE)
    
    done = False
    server_list = []
    activated_list = []

    addr_lst = list()
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.settimeout(1)
        while not done:
            size = screen.get_size()
            if size[0] < size[1]:
                length = size[0]
            else:
                length = size[1]
            vl = length / 100
            offsetx = int((size[0] - length) / 2)
            offsety = int((size[1] - length) / 2)

            font = pg.font.SysFont('Courier New', int(3.2 * vl))
            
            reload = font.render('Refresh', True, Color.green, Color.blue)
            reload_size = reload.get_rect().size

            play = font.render('PLAY!', True, Color.grey_blue, Color.grey_green)
            play_size = play.get_rect().size

            list_box = Rect(offsetx + int(14 * vl), offsety + int(6 * vl), int(72 * vl), int(80 * vl))


            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if offsetx + length / 2 - (reload_size[0] + play_size[0] + int(4 * vl)) / 2 <= pg.mouse.get_pos()[0] <= offsetx + length / 2 - play_size[0] / 2 - int(4 * vl) + reload_size[0] / 2 and offsety + int(90 * vl) <= pg.mouse.get_pos()[1] <= offsety + int(90 * vl) + reload_size[1]:
                            addr_lst = []
                            server_list = []
                            activated_list = []
                        elif offsetx + int(14 * vl) <= pg.mouse.get_pos()[0] <= offsetx + int(86 * vl) and offsety + int(6 * vl) <= pg.mouse.get_pos()[1] <= offsety + int(86 * vl):
                            if not int((pg.mouse.get_pos()[1] - int(6 * vl)) / 25 + offsety) > len(server_list) - 1:
                                if True in activated_list:
                                    activated_list[activated_list.index(True)] = False
                                activated_list[int((pg.mouse.get_pos()[1] - int(6 * vl)) / 25 + offsety)] = True

                        elif offsetx + length / 2 - play_size[0] / 2 + reload_size[0] / 2 + int(2 * vl) <= pg.mouse.get_pos()[0] <= offsetx + length / 2 + (reload_size[0] + play_size[0] + int(4 * vl)) / 2 and offsety + int(90 * vl) <= pg.mouse.get_pos()[1] <= offsety + int(90 * vl) + reload_size[1] and True in activated_list:
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

            received[0] = None
            screen.fill(Color.black)

            for index, server in enumerate(server_list):
                server_text = font.render(server, True, (Color.green, Color.blue)[index % 2])
                server_rect = Rect(offsetx + int(15 * vl), offsety + int(7 * vl) + index * int(5 * vl), int(70 * vl), int(5 * vl))
                if activated_list[index]:
                    pg.draw.rect(screen, (Color.blue, Color.green)[index % 2], server_rect)
                else:
                    pg.draw.rect(screen, (Color.blue, Color.green)[index % 2], server_rect, int(1 + 0.6 * vl))
                screen.blit(server_text, (server_rect.x + int(1 + 1 * vl), server_rect.y + int(1 + 1 * vl)))

            if True in activated_list:
                play = font.render('PLAY!', True, Color.blue, Color.green)

            pg.draw.rect(screen, Color.white, list_box, int(1 + 1 * vl))
            screen.blit(reload, (offsetx + length / 2 - (reload_size[0] + play_size[0] + int(4 * vl)) / 2, offsety + int(90 * vl)))
            screen.blit(play, (offsetx + length / 2 - play_size[0] / 2 + reload_size[0] / 2 + int(2 * vl), offsety + int(90 * vl)))
            pg.display.update()
        
        return 'QUIT'

if __name__ == '__main__':
    pg.init()
    ipv4_host = server_finder()
    pg.quit()
    if ipv4_host == 'QUIT':
        sys.exit()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print((ipv4_host, ipv4_port))
        s.connect((ipv4_host, ipv4_port))
        snake_color_lst = []
        pg.init()
        done = False
        screen = pg.display.set_mode((500, 500), pg.RESIZABLE)
        clock = pg.time.Clock()
        ready = False
        snake_color = Color.white
        s.sendall(b'Hello')
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

            lobby = font.render(' Lobby ', True, Color.green, Color.blue)
            lobby_size = lobby.get_rect().size

            ready_txt = font.render(' Ready ', True, Color.blue, Color.green)
            ready_size = ready_txt.get_rect().size

            rect = Rect(offsetx + length / 2 - int(80 * vl) / 2, offsety + int(18 * vl), int(80 * vl), int(60 * vl))
            data = s.recv(4096)
            if data:
                data_buffer += data
            if len(data_buffer) >= 2:
                hdr = struct.unpack('>H', data_buffer[:2])[0]
                snake_num = hdr >> 13
                body_len = hdr >> 8 & 0b11111
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
                    if len(snake_color_lst) > snake_num:
                        snake_color = snake_color_lst[snake_num]

            screen.fill(Color.black)
            snk_num = len(snake_color_lst)
            screen.blit(lobby, (offsetx + length / 2 - lobby_size[0] / 2, offsety + int(2 * vl)))
            screen.blit(ready_txt, (offsetx + length / 2 - ready_size[0] / 2, offsety + int(80 * vl)))

            snk = Rect(offsetx + length / 2 - (snk_num * int(5 * vl) + (snk_num - 1) * int(5 * vl)) / 2, offsety + int(50 * vl), int(5 * vl), int(28 * vl))

            ready_snake_num = 0
           
            for i in range(snk_num):
                if (ready_snakes << i & 0xff) >> 7 == 1:
                    snk.y = offsety + int(35 * vl)
                    snk.size = (snk.size[0], int(43 * vl))
                    ready_snake_num += 1
                else:
                    snk.y = offsety + int(50 * vl)
                    snk.size = (snk.size[0], int(28 * vl))
                    
                pg.draw.rect(screen, snake_color_lst[i], snk)
                
                snk.x += int(10 * vl)

            # Draw outline
            pg.draw.rect(screen, snake_color, rect, 1)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    if offsetx + length / 2 - ready_size[0] / 2 <= pg.mouse.get_pos()[0] <= offsetx + length / 2 + ready_size[0] / 2 and offsety + int(80 * vl) <= pg.mouse.get_pos()[1] <= offsety + int(80 * vl) + ready_size[1]:
                        ready = True
                        ready_txt = font.render(' Ready ', True, Color.green, Color.blue)


            if ready:
                s.sendall(b'r')
            else:
                s.sendall(b'n')

            pg.display.flip()
            clock.tick(100) 
        pg.quit()
        sys.exit()