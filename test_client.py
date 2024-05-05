import json
import logging
import threading

from client.client_class import Client
from net.package_classes.package_headers import PackageHeader

logging.basicConfig(level=logging.DEBUG)

server_addr = 'localhost'
server_port = int(input('Введите порт: '))

client = Client()

client_thread = threading.Thread(target=client.connect, args=(server_addr, server_port))
client_thread.start()

while client.is_active:
    command = input('>')

    if command == 'join':
        username = input('Введите имя: ')
        client.join_to_lobby_as(username)
    elif command == 'exit':
        client.disconnect()
    elif command == 'users':
        client.send_security_content_to_server(PackageHeader.GetUsersInLobby,
                                               b'0')
    elif command == 'connect_to':
        to_username = input(f'Введите имя собеседника: ')

        client.send_security_content_to_server(PackageHeader.GetCommonKeyForUser,
                                               json.dumps({'to_username': to_username}).encode())
    elif command == 'msg':
        to_username = input(f'Введите имя собеседника: ')
        message = input(f'Введите сообщение: ')

        client.send_security_content_to_client(PackageHeader.SendMessageToUser,
                                               to_username,
                                               message.encode())


print('!')
client_thread.join()
