import socket, select

CONNECTION_LIST = []  # list of socket clients
RECV_BUFFER = 1024  # Advisable to keep it as an exponent of 2
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", PORT))
server_socket.listen(10)


# def broadcast_data(sock, message):
#     for socket in CONNECTION_LIST:
#         if socket != server_socket:
#             try:
#                 socket.send(message.encode('utf-8'))
#             except:
#                 socket.close()
#                 CONNECTION_LIST.remove(socket)


CONNECTION_LIST.append(server_socket)
p = None
while True:
    read_socket, write_socket, error = select.select(CONNECTION_LIST, [], [])

    for sock in read_socket:

        if sock == server_socket:
            print('Server starts ... ')
            sockfd, addr = server_socket.accept()

            CONNECTION_LIST.append(sockfd)
            print('Client {} connected'.format(addr))

        else:
            try:
                p = sock.getpeername()[1]
            except:
                continue
            try:
                data = sock.recv(RECV_BUFFER)
                # 'q'为退出判断字符
                if data.decode('utf-8') != 'q':
                    msg = '{} ===>'.format(p) + data.decode('utf-8')
                    sock.send(msg.encode('utf-8'))
                else:
                    # broadcast_data(sock, "Client {} is offline".format(p))
                    print("Client {} is offline".format(p))
                    sock.close()
                    CONNECTION_LIST.remove(sock)


            except:
                # broadcast_data(sock, "Client {} is offline".format(p))
                print("Client {} is offline".format(p))
                sock.close()
                CONNECTION_LIST.remove(sock)



server_socket.close()