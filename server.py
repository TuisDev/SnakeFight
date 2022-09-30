import socket
import struct
import time
import sys
import threading
import pygame as pg
from pygame.locals import *
from servergame import player_color, Color

computer_name = socket.gethostname()
ipv6_multicast = "ff02::face:1"
ipv6_port = 65431
ipv4_host = socket.gethostbyname(computer_name)
ipv4_port = 65432
start_time = time.time()
snake_color_lst = [[player_color.blue]]
ready_snakes = [0b00000000]

def look_for_clients():
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as udp_sock:
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_sock.bind(('', ipv6_port))
        # udp_sock.setblocking(False)
        mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, ipv6_multicast), (chr(0) * 16).encode('utf-8'))
        udp_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        while True:
            data, addr = udp_sock.recvfrom(1024)
            
            if data == b'I want to play snake':
                udp_sock.sendto(f'{computer_name}, {ipv4_host}'.encode(), addr)
                print(f'send data to {addr}')

def tcp_server(conn, snake_num):
    with data_lock:
        data = conn.recv(1024)
        print(f'scl = {snake_color_lst}')
        print(snake_color_lst)
        snake_color_lst[0].append(list(player_color.translate)[len(snake_color_lst[0])])
    while True:
        body_len = len(snake_color_lst[0]) * 3
        hdr = struct.pack('>H', (snake_num << 4 | body_len) << 8 | ready_snakes[0])
        conn.sendall(hdr)
        print(hdr)
        for rgb in snake_color_lst[0]:
            for color in rgb:
                color_bin = struct.pack('>B', color)
                print(f'color_bin = {color_bin}')
                conn.send(color_bin)
        if len(data) == 7:
            break
        time.sleep(0.1)
    conn.close()

def tcp_wait_for_client(socket):
    snake_num = 0
    while True:
        time.sleep(0.05)
        conn, addr = socket.accept()
        snake_num += 1
        print(f'Connected at {addr}')
        threading.Thread(target=tcp_server, args=(conn, snake_num), daemon=True).start()

if __name__ == '__main__':
    threading.Thread(target=look_for_clients, args=(), daemon=True).start()
    
    data_lock = threading.Lock()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            print(f'THIS {(ipv4_host, ipv4_port)}')
            s.bind((ipv4_host, ipv4_port))
            s.listen(7)
            tcp_accept = threading.Thread(target=tcp_wait_for_client, args=(s,), daemon=True)
            tcp_accept.start()
            pg.init()
            done = False
            size = 500, 500
            width, height = size
            screen = pg.display.set_mode((size))
            clock = pg.time.Clock()
            font = pg.font.Font('freesansbold.ttf', 32)

            lobby = font.render(' Lobby ', True, Color.green, Color.blue)
            lobby_size = lobby.get_rect().size

            ready = font.render(' Ready ', True, Color.blue, Color.green)
            ready_size = lobby.get_rect().size

            rect = Rect(width / 2 - 400 / 2, 90, 400, 300)

            snk = Rect(width / 2 - 25 / 2, 250, 25, 140)
            snk_num = 6            
            x1pos = width / 2 - 25 / 2
            x2pos = width / 2 + 25 / 2

            while not done:
                screen.blit(lobby, (width / 2 - lobby_size[0] / 2, 10))
                screen.blit(ready, (width / 2 - ready_size[0] / 2, 400))

                pg.draw.rect(screen, Color.white, rect, 1)
                snk = Rect(width / 2 - (snk_num * 25 + (snk_num - 1) * 25) / 2, 250, 25, 140)
                x1pos = (width / 2 - (snk_num * 25 + (snk_num - 1) * 25) / 2)
                x2pos = (width / 2 - (snk_num * 25 + (snk_num - 1) * 25 ) / 2 + 25)

                for i in range(snk_num):
                    pg.draw.rect(screen, Color.blue, snk)
                    pg.draw.line(screen, Color.red, (x1pos, 50), (x2pos, 80), 5)
                    pg.draw.line(screen, Color.red, (x1pos, 80), (x2pos, 50), 5)

                    snk.x += 50
                    x1pos += 50
                    x2pos += 50
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                
                pg.display.flip()
                clock.tick(100)
                
            pg.quit()
            sys.exit()
            tcp_accept.join()
        except KeyboardInterrupt:
            print('BYEBYEBYE')