
import socket
import sys

computer_name = socket.gethostname()
ipv6_multicast = "ff02::face:1"
ipv6_port = 65431
ipv4_host = ''
ipv4_port = 65432

with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as udp_sock:

    while True:
        udp_sock.sendto("I want to play snake".encode(), (ipv6_multicast, ipv6_port))
        received = udp_sock.recvfrom(1024)
        data = received[0].decode()
        addr = received[1]
        server_name, ipv4_host = data.split(', ')

        if received:
            print(f'Play on {server_name}')
            break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print((ipv4_host, ipv4_port))
s.connect((ipv4_host, ipv4_port))
s.close()
# cd onedrive/documents/coding/python