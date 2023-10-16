import socket
import struct
import threading

SO_ORIGINAL_DST = 80


class SocketClient(object):

    def __init__(self, dst_ip: str, dst_port: int):
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("remote addr = ", (dst_ip, dst_port))
        self.client.connect((dst_ip, dst_port))

    def send(self, content: bytes):
        self.client.sendall(content)
        print("发送完成")

    def receive(self):
        print("start to recv...")
        result = b""
        while True:
            resp = self.client.recv(1024)
            print("resp=", resp)
            result += resp
            if len(resp) < 1024:
                break
        return result

    def close(self):
        self.client.close()


def proxy_handler(conn: socket.socket, addr):
    print("Accept new connection from %s:%s" % addr)
    dst = conn.getsockopt(socket.SOL_IP, SO_ORIGINAL_DST, 16)
    dst_port, dst_ip = struct.unpack("!2xH4s8x", dst)
    dst_ip = socket.inet_ntoa(dst_ip)
    print("真实的目标IP=", dst_ip)
    print("真实的目标Port=", dst_port)
    remote_client = SocketClient(dst_ip=dst_ip, dst_port=int(dst_port))
    while True:
        content = conn.recv(1024)
        if content in (b"", b"exit"):
            conn.send(b"exit")
            break
        print("receive: ", content)
        remote_client.send(content)
        resp = remote_client.receive()
        print("remote resp=", resp)
        conn.send(resp)
    conn.close()
    remote_client.close()
    print("Connection from %s:%s is closed" % addr)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 一般来说，一个端口释放后会等待两分钟之后才能再被使用，SO_REUSEADDR是让端口释放后立即就可以被再次使用。
# server程序总是应该在调用bind()之前设置SO_REUSEADDR套接字选项
# 这个套接字选项通知内核，如果端口忙，但TCP状态位于 TIME_WAIT ，可以重用端口。
# 如果端口忙，而TCP状态位于其他状态，重用端口时依旧得到一个错误信息，指明"地址已经使用中"。
# 如果你的服务程序停止后想立即重启，而新套接字依旧使用同一端口，此时SO_REUSEADDR 选项非常有用。
# 必须意识到，此时任何非期望数据到达，都可能导致服务程序反应混乱，不过这只是一种可能，事实上很不可能。
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("127.0.0.1", 5008))
s.listen(5)
print("Waiting for connection...")

while True:
    conn, addr = s.accept()
    # t = threading.Thread(target=proxy_handler, args=(conn, addr))
    # t.start()
    proxy_handler(conn, addr)
