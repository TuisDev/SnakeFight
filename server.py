
import socket
import struct
import sys

computer_name = socket.gethostname()
ipv6_multicast = "ff02::face:1"
ipv6_port = 65431
ipv4_host = socket.gethostbyname(computer_name)
ipv4_port = 65432


with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as udp_sock:
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(('', ipv6_port))
    mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, ipv6_multicast), (chr(0) * 16).encode('utf-8'))
    udp_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    while True:
        data, addr = udp_sock.recvfrom(1024)
        
        if data == b'I want to play snake':
            udp_sock.sendto(f'{computer_name}, {ipv4_host}'.encode(), addr)
            break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print((ipv4_host, ipv4_port))
s.bind((ipv4_host, ipv4_port))
s.listen()
conn, adr = s.accept()
s.close()