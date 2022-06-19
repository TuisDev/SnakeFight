
import socket
import struct
import time
import sys
import threading

computer_name = socket.gethostname()
ipv6_multicast = "ff02::face:1"
ipv6_port = 65431
ipv4_host = socket.gethostbyname(computer_name)
ipv4_port = 65432
start_time = time.time()

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

def tcp_server(conn):

    while True:
        data_lock.acquire()
        data = conn.recv(1024)
    
        if data is None:
            data_lock.release()
            break
            
        conn.sendall(data)
        data_lock.release()
        time.sleep(0.1)
    conn.close()



if __name__ == '__main__':
    threading.Thread(target=look_for_clients, args=(), daemon=True).start()
    


    data_lock = threading.Lock()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            print((ipv4_host, ipv4_port))
            s.bind((ipv4_host, ipv4_port))
            s.listen()
            while True:
                conn, addr = s.accept()
                print(f'Connected at {addr}')
                threading.Thread(target=tcp_server, args=(conn,), daemon=True).start()
                if start_time - time.time() > 15:
                    break
        except KeyboardInterrupt:
            print('BYEBYEBYE')