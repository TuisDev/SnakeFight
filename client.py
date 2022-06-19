
import socket
import sys
import pygame as pg
from game import player_color
import threading
import time

computer_name = socket.gethostname()
ipv6_multicast = "ff02::face:1"
ipv6_port = 65431
ipv4_host = [None, None]
ipv4_port = 65432
start_time = time.time()

def find_games():
    addr_lst = list()
    socket.setdefaulttimeout(1)
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as udp_sock:

        try:
            while True:
                udp_sock.sendto("I want to play snake".encode(), (ipv6_multicast, ipv6_port))
                received = udp_sock.recvfrom(1024)
                data = received[0].decode()
                addr = received[1]
                server_name, ipv4_host[0] = data.split(', ')

                if received is not None and addr not in addr_lst:
                    print(f'Play on {server_name}')
                    addr_lst.append(addr)
                if time.time() - start_time > 2:
                    return
        except:
            return
            

def color_picker():
    pass

def main():
    pass

udp = threading.Thread(target=find_games(), args=(), daemon = True)
udp.start()



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print((ipv4_host[0], ipv4_port))
    s.connect((ipv4_host[0], ipv4_port))
    while True:
        s.sendall(b'BANANANANA')
        data = s.recv(1024)

        print(f'Received from the server : {data.decode()}')

        time.sleep(1)
# cd onedrive/documents/coding/python