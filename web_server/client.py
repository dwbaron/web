import socket
import time


def Client():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('', 5000))  # 链接服务器
    # 获得自己的地址
    port = sock.getsockname()[1]
    while True:
        print('enter something:')
        ent = input()
        if ent == '':
            break
        sock.send(ent.encode('utf-8'))  # 发送数据给服务器
        time.sleep(1)
        data = sock.recv(1024)  # 接收服务器发过来到数据
        data = data.decode('utf-8')

        print(data[7:12])
        # 根据服务器返回判断退出
        if ('offline' in data and port == data[7:12]) or not data:
            print('closing ... ')
            sock.close()
            return
        print('echo=>', data)
    sock.close()


if __name__ == '__main__':
    Client()