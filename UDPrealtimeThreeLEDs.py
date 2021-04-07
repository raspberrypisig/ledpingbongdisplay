#!/usr/bin/env python3

import socket

#UDP_IP_ADDRESS = "192.168.8.166"
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 21324

v = [2, 2, 255, 0, 0, 0, 255, 0, 0, 0, 255]
Message = bytearray(v)

clientSock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto (Message, (UDP_IP_ADDRESS, UDP_PORT_NO))