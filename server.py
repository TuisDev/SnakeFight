'''
	Simple udp socket server
'''

import socket
import struct
import sys

computer_name = socket.gethostname()
ipv6_host = '111111'
ipv6_port = 65431
ipv4_host = socket.gethostbyname(computer_name)


with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as udp_sock:
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(('', ipv6_port))
    udp_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
    mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, "ff02::abcd:1"), (chr(0) * 16).encode('utf-8'))
    udp_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    while True:
        data, addr = udp_sock.recvfrom(1024)
        
        if data == b'I want to play snake':
            udp_sock.sendto(f'{computer_name}, {ipv4_host}'.encode(), addr)
            break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print((ipv4_host, 65432))
s.bind((ipv4_host, 65432))
s.listen()
conn, adr = s.accept()
s.close()