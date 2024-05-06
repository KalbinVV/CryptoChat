import logging
import random
import socket
import threading
from typing import Optional, NoReturn

from net.connection_class import Connection
from net.package_classes.insecure_package_class import InsecurePackage
from net.package_classes.package_headers import PackageHeader
from net.package_classes.package_types import PackageType
from server.stages.stages_dict import get_stage
from utils.async_utils import AsyncFlag


class CryptoChatServer:
    def __init__(self):
        self.__server_socket = socket.socket(socket.AF_INET)
        self.__server_is_running = AsyncFlag(value=False)
        self.__connections: list[Connection] = []
        self.__connections_threads: list[threading.Thread] = []

        self.__usernames_connection_dict: dict[str, Connection] = dict()
        self.__connection_username_dict: dict[Connection, str] = dict()

        self.storage = dict()

    def update_username(self, connection: Connection, username: str) -> None:
        self.__usernames_connection_dict[username] = connection
        self.__connection_username_dict[connection] = username

    def get_connection_by_username(self, username: str) -> Optional[Connection]:
        return self.__usernames_connection_dict.get(username, None)

    def get_username_by_connection(self, connection: Connection) -> Optional[str]:
        return self.__connection_username_dict.get(connection, None)

    def get_users_in_lobby(self):
        return list(self.__usernames_connection_dict.keys())

    def start(self) -> Optional[NoReturn]:
        server_port = random.randint(1050, 10000)

        try:
            self.__server_socket.bind(('', server_port))
            self.__server_socket.listen(1)

            self.__server_is_running.value = True

            logging.info(f'Сервер запущен по адресу: {self.__server_socket.getsockname()}')

            self.__start_accepting_connections()
        except (Exception, ) as e:
            logging.critical(f'Не удалось запустить сервер: {e}')
            self.start()

    def __start_accepting_connections(self) -> None:
        logging.info(f'Сервер ожидает новые соединения...')

        while self.__server_is_running.value:
            server_socket, addr = self.__server_socket.accept()

            connection = Connection(server_socket, addr)

            self.__connections.append(connection)

            connection.storage['server'] = self

            logging.info(f'Новое подключение: {connection.address}')

            connection_thread = threading.Thread(target=self.__start_connection_processing,
                                                 args=(connection,))

            connection_thread.start()

            self.__connections_threads.append(connection_thread)

    def __start_connection_processing(self, connection: Connection) -> Optional[NoReturn]:
        while connection.is_alive and self.__server_is_running.value:
            logging.debug(f'{connection.address} now waiting packages...')

            package = connection.receive_package()

            logging.debug(f'Package {package} from {connection.address}')

            if package.header == PackageHeader.Disconnected:
                connection.is_alive = False

                logging.info(f'{connection.address} отключился от сессии')

                self.__connections.remove(connection)

                username = self.__connection_username_dict[connection]

                del self.__connection_username_dict[connection]
                del self.__usernames_connection_dict[username]
            else:
                if package.package_type == PackageType.SecureCommunicateBetweenClients:
                    self.__resend_to_client(package)
                    continue

                stage = get_stage(package.header)
                stage.process(connection, package)

    def __resend_to_client(self, package) -> None:
        to_username = package.to_username

        connection = self.get_connection_by_username(to_username)

        if connection is None:
            logging.info(f'Неизвестный получатель: {to_username}, исключаем пакет.')
            return

        logging.info(f'Get package from: {package.from_username}')

        connection.send_secure_content_by_server_communicate(package.header,
                                                             package.content,
                                                             connection.storage['common_key'],
                                                             package.from_username)

        logging.info(f'Sent package to {self.__connection_username_dict[connection]}')

    def stop(self) -> Optional[NoReturn]:
        self.__server_is_running.value = False
        self.__server_socket.close()

        for connection in self.__connections:
            connection.send_package(InsecurePackage(header=PackageHeader.Disconnected,
                                                    content=b''))

        for thread in self.__connections_threads:
            thread.join()

        logging.info(f'Сервер остановлен')
