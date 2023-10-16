import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 5000))

while True:
    data = input("Please input something: ")
    if not data:
        continue
    s.send(data.encode())
    resp = s.recv(1024).decode()
    if resp == "exit":
        break

s.close()
"""
iptables -t nat -A OUTPUT -p tcp -d 192.168.1.101 --dport 1234 -j DNAT --to-destination 192.168.1.102:4321
"""
