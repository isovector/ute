from ute import Message
import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(Message("new").toJson(), ("localhost", 6112))
