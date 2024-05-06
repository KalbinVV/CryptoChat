# Класс для работы с текущими соединениями
import json
import logging
import socket
import threading
import time
from typing import Optional

from net.package_classes.package_builder import PackageBuilder
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader
from net.package_classes.package_types import PackageType
from utils.async_utils import AsyncFlag

from Crypto.Cipher import AES

from utils.security_utils import get_nonce


class Connection:
    def __init__(self, connection_socket: socket.socket, address: tuple[str, int]):
        self.__connection_socket = connection_socket
        self.__address = address
        self.__is_alive = AsyncFlag(value=True)
        self.storage = dict()

        self.__lock = threading.Lock()

    def send_raw(self, content: bytes | int) -> None:
        self.__connection_socket.send(content)

    def send_package(self, package: Package, encrypt: bool = True) -> None:
        package.send(self, encrypt)

    def send_secure_content_by_server_communicate(self, header: PackageHeader,
                                                  content: bytes, common_key: bytes,
                                                  from_username: Optional[str] = None):
        from net.package_classes.secure_package_by_communicate_with_server_class \
            import SecurePackageByCommunicateWithServer

        package = SecurePackageByCommunicateWithServer(header, content, common_key, from_username)
        self.send_package(package)

    def receive_package(self):
        with self.__lock:
            header_size = self.__connection_socket.recv(10)

            logging.debug(f'Header size {header_size} from {self.address}')

            if not header_size:
                from net.package_classes.insecure_package_class import InsecurePackage
                return InsecurePackage(header=PackageHeader.Disconnected,
                                       content=b'')

            package_header_raw = self.__connection_socket.recv(int(header_size.decode()))
            package_header = json.loads(package_header_raw.decode())

            logging.debug(f'Header {package_header_raw} from {self.address}')

            package_type = PackageType[package_header['type']]

            content_length = int(package_header['content_length'])

            if not package_type.is_secure():
                content = self.__get_insecure_content(content_length)
            else:
                if package_type == PackageType.SecureCommunicateWithServer:
                    tag_length = package_header['tag_length']

                    content = self.__get_secure_content_by_server(tag_length, content_length)
                else:
                    content = self.__get_secure_content_by_server(0, content_length)

            return PackageBuilder.from_header(package_header,
                                              content)

    def __get_insecure_content(self, content_length: int) -> bytes:
        return self.__connection_socket.recv(content_length)

    def __get_secure_content_by_server(self, tag_length: int, content_length: int) -> bytes:
        if 'common_key' not in self.storage:
            raise Exception('Данные невозможно получить, безопасное соединение не установлено!')

        nonce = get_nonce()

        common_key = self.storage.get('common_key')

        if tag_length > 0:
            tag = self.__connection_socket.recv(tag_length)
            logging.debug(f'Tag: {tag}')

        content = self.__connection_socket.recv(content_length)
        logging.debug(f'Raw content: {content}')

        decipher = AES.new(common_key, AES.MODE_EAX, nonce)

        decrypted_content = decipher.decrypt(content)

        logging.debug(f'Decrypted content: {decrypted_content}')

        return decrypted_content

    @property
    def address(self) -> tuple[str, int]:
        return self.__address

    @property
    def is_alive(self) -> bool:
        return self.__is_alive.value

    @is_alive.setter
    def is_alive(self, value: bool) -> None:
        self.__is_alive.value = value
