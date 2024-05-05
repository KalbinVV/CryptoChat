import json
import logging
import socket
from typing import Optional

from net.connection_class import Connection
from net.package_classes.insecure_package_class import InsecurePackage
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader
from net.package_classes.secure_package_for_clients_communication_class import SecurePackageForClientsCommunication
from utils.async_utils import AsyncFlag


class Client:
    def __init__(self):
        self.__client_socket = socket.socket()
        self.__server_connection: Optional[Connection] = None
        self.__server_is_active = AsyncFlag(value=False)

        self.__sessions_key: dict[str, bytes] = dict()

        self.storage = dict()

        self.__username = ''

    def connect(self, address: str, port: int) -> None:
        self.__client_socket.connect((address, port))

        self.__server_is_active.value = True

        self.__server_connection = Connection(self.__client_socket, (address, port))

        self.send(InsecurePackage(header=PackageHeader.FirstConnect,
                                  content=b''))

        self.__wait_packages_from_server()

    def get_server_storage(self):
        return self.__server_connection.storage

    def update_username(self, username: str):
        self.__username = username

    def join_to_lobby_as(self, username: str):
        content = json.dumps({'username': username}).encode()
        common_key = self.get_server_storage()['common_key']

        self.__server_connection.send_secure_content_by_server_communicate(PackageHeader.JoinToLobby,
                                                                           content,
                                                                           common_key)

    def update_session_key(self, username: str, session_key: bytes) -> None:
        self.__sessions_key[username] = session_key

    def get_session_key_for_username(self, username: str) -> Optional[bytes]:
        return self.__sessions_key.get(username, None)

    def __wait_packages_from_server(self):
        while self.__server_is_active.value:
            package = self.__server_connection.receive_package()

            logging.debug(f'Получен пакет: {package}')

            if package.header == PackageHeader.Disconnected:
                logging.info('Соединение с сервером потеряно')

                self.disconnect()
            else:
                from client.stages.client_stages_dict import get_stage

                stage = get_stage(package.header)
                stage.process_package(self, package)

    def send(self, package: Package):
        self.__server_connection.send_package(package)
        
    def send_security_content_to_server(self, header: PackageHeader, content: bytes):
        if 'common_key' not in self.get_server_storage():
            raise Exception('Невозможно отправить защищенные данные, безопасное соединение не установлено!')

        common_key = self.get_server_storage()['common_key']

        self.__server_connection.send_secure_content_by_server_communicate(header, content, common_key)

    def send_security_content_to_client(self, header: PackageHeader,
                                        to_username: str,
                                        content: bytes):
        if 'common_key' not in self.get_server_storage():
            raise Exception('Невозможно отправить защищенные данные, безопасное соединение не установлено!')

        common_key = self.get_server_storage()['common_key']

        session_key = self.get_session_key_for_username(to_username)

        if not session_key:
            logging.error(f'Нельзя отправить сообщение {to_username}, вы не установили с ним безопасное соединение!')

        package = SecurePackageForClientsCommunication(header,
                                                       content,
                                                       self.__username,
                                                       to_username,
                                                       common_key,
                                                       session_key)

        self.__server_connection.send_package(package)

    @property
    def is_active(self):
        return self.__server_is_active.value

    def disconnect(self) -> None:
        if self.__server_is_active.value:
            self.__server_connection.send_package(InsecurePackage(header=PackageHeader.Disconnected,
                                                                  content=b''))

            self.__server_is_active.value = False
            self.__client_socket.close()
