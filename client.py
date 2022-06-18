
import socket	#for sockets
import sys

computer_name = socket.gethostname()
ipv6_host = "ff02::abcd:1"
ipv6_port = 65431

with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as udp_sock:
    udp_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)

    while True:
        udp_sock.sendto("I want to play snake".encode(), (ipv6_host, ipv6_port))
        received = udp_sock.recvfrom(1024)
        data = received[0].decode()
        addr = received[1]
        server_name, ip = data.split(', ')

        if received:
            print(f'Play on {server_name}')
            break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print((ip, 65432))
s.connect((ip, 65432))
s.close()
# cd onedrive/documents/coding/python