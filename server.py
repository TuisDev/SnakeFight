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
banned_snakes = [[0]]
is_ready = False

def look_for_clients():
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as udp_sock:
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_sock.bind(('', ipv6_port))
        # udp_sock.setblocking(False)
        mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, ipv6_multicast), (chr(0) * 16).encode('utf-8'))
        udp_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        while True:
            data, addr = udp_sock.recvfrom(1024)
            
            if data == b'I want to play snake' and len(snake_color_lst[0]) < 7:
                udp_sock.sendto(f'{computer_name}, {ipv4_host}'.encode(), addr)
                print(f'send data to {addr}')

def tcp_server(conn, snake_num):
    try:
        with data_lock:
            data = conn.recv(1024)
            snake_color_lst[0].append([color for color in list(player_color.translate) if color not in snake_color_lst[0]][0])
        while True:
            if banned_snakes[0][0] == snake_num:
                with data_lock:
                    banned_snakes[0][0] = 0
                    ready_snakes[0] = ready_snakes[0] & 0b111111101111111 >> snake_num
                break
            while snake_num in banned_snakes[0] and banned_snakes[0][0] == 0:
                with data_lock:
                    banned_snakes[0][banned_snakes[0].index(snake_num)] += 1    
                snake_num -= 1

            body_len = len(snake_color_lst[0]) * 3
            hdr = struct.pack('>H', (snake_num << 5 | body_len) << 8 | ready_snakes[0])
            
            conn.sendall(hdr)
            for rgb in snake_color_lst[0]:
                for color in rgb:
                    color_bin = struct.pack('>B', color)
                    conn.send(color_bin)
            if len(data) == 7:
                break
            data = conn.recv(1024)
            if data[:1] == b'r':
                with data_lock:
                    ready_snakes[0] = ready_snakes[0] | 0b10000000 >> snake_num

            time.sleep(0.1)
    except ConnectionResetError:
        with data_lock:
            ready_snakes[0] = ready_snakes[0] & 0b111111101111111 >> snake_num
            del snake_color_lst[0][snake_num]
            banned_snakes[0].insert(1, snake_num + 1)
    conn.close()

def tcp_wait_for_client(socket):
    snake_num = 0
    while True:
        time.sleep(0.05)
        conn, addr = socket.accept()
        if len(snake_color_lst[0]) >= 7:
            conn.close()
            continue
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
            s.listen(20)
            tcp_accept = threading.Thread(target=tcp_wait_for_client, args=(s,), daemon=True)
            tcp_accept.start()
            pg.init()
            done = False
            screen = pg.display.set_mode((500, 500), pg.RESIZABLE)
            clock = pg.time.Clock()
            

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

                play_txt = font.render(' Play ', True, Color.blue, Color.green)
                play_size = play_txt.get_rect().size

                rect = Rect(offsetx + length / 2 - int(80 * vl) / 2, offsety + int(18 * vl), int(80 * vl), int(60 * vl))

                screen.fill(Color.black)
                snk_num = len(snake_color_lst[0])

                snk = Rect(offsetx + length / 2 - (snk_num * int(5 * vl) + (snk_num - 1) * int(5 * vl)) / 2, offsety + int(50 * vl), int(5 * vl), int(28 * vl))
                x1pos = offsetx + (length / 2 - (snk_num * int(5 * vl) + (snk_num - 1) * int(5 * vl)) / 2)
                x2pos = offsetx + (length / 2 - (snk_num * int(5 * vl) + (snk_num - 1) * int(5 * vl) ) / 2 + int(5 * vl))

                ready_snake_num = 0

                for i in range(snk_num):
                    if (ready_snakes[0] << i & 0xff) >> 7 == 1:
                        snk.y = offsety + int(35 * vl)
                        snk.size = (snk.size[0], int(43 * vl))
                        ready_snake_num += 1
                    else:
                        snk.y = offsety + int(50 * vl)
                        snk.size = (snk.size[0], int(28 * vl))
                    
                    
                    pg.draw.rect(screen, snake_color_lst[0][i], snk)
                    

                    if i > 0:
                        pg.draw.line(screen, Color.red, (x1pos, offsety + int(10 * vl)), (x2pos, offsety + int(16 * vl)), int(1 * vl))
                        pg.draw.line(screen, Color.red, (x1pos, offsety + int(16 * vl)), (x2pos, offsety + int(10 * vl)), int(1 * vl))

                    snk.x += int(10 * vl)
                    x1pos += int(10 * vl)
                    x2pos += int(10 * vl)

                # Draw Text
                screen.blit(lobby, (offsetx + length / 2 - lobby_size[0] / 2, offsety + int(2 * vl)))

                if ready_snake_num == snk_num:
                    screen.blit(play_txt, (offsetx + length / 2 - play_size[0] / 2, offsety + int(80 * vl)))
                else:
                    screen.blit(ready_txt, (offsetx + length / 2 - ready_size[0] / 2, offsety + int(80 * vl)))

                # Draw Outline
                pg.draw.rect(screen, Color.blue, rect, int(1 + 0.2 * vl))

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if ready_snake_num == snk_num:
                            if offsetx + length / 2 - play_size[0] / 2 <= pg.mouse.get_pos()[0] <= offsetx + length / 2 + play_size[0] / 2 and offsety + int(80 * vl) <= pg.mouse.get_pos()[1] <= offsety + int(80 * vl) + play_size[1]:
                                print("PLAY")
                        else:
                            # Ready Button
                            if offsetx + length / 2 - play_size[0] / 2 <= pg.mouse.get_pos()[0] <= offsetx + length / 2 + ready_size[0] / 2 and offsety + int(80 * vl) <= pg.mouse.get_pos()[1] <= offsety + int(80 * vl) + ready_size[1]:
                                ready_snakes[0] = ready_snakes[0] | 0b10000000
                                ready_txt = font.render(' Ready ', True, Color.green, Color.blue)

                            # Ban button
                            x1pos = offsetx + (length / 2 - (snk_num * int(5 * vl) + (snk_num - 1) * int(5 * vl)) / 2)
                            x2pos = offsetx + (length / 2 - (snk_num * int(5 * vl) + (snk_num - 1) * int(5 * vl) ) / 2 + int(5 * vl))
                            for i in range(snk_num):
                                if i > 0:
                                    if x1pos <= pg.mouse.get_pos()[0] <= x2pos and offsety + int(10 * vl) <= pg.mouse.get_pos()[1] <= offsety + int(16 * vl):
                                        del snake_color_lst[0][i]
                                        banned_snakes[0][0] = i
                                        banned_snakes[0].insert(1, i + 1)
                                x1pos += int(10 * vl)
                                x2pos += int(10 * vl)


                pg.display.flip()
                clock.tick(100)
                
                
            pg.quit()
            sys.exit()
            tcp_accept.join()
        except KeyboardInterrupt:
            print('BYEBYEBYE')