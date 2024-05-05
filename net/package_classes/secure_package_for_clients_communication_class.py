import json
from typing import Optional

from Crypto.Cipher import AES

from net.connection_class import Connection
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader
from net.package_classes.package_types import PackageType
from utils.security_utils import get_nonce


class SecurePackageForClientsCommunication(Package):
    def __init__(self, header: PackageHeader,
                 content: bytes,
                 from_username: str,
                 to_username: str,
                 common_key_for_server: Optional[bytes] = None,
                 common_key_between_clients: Optional[bytes] = None):
        super().__init__(PackageType.SecureCommunicateBetweenClients,
                         header,
                         content,
                         tag=None)

        self.__common_key_for_server = common_key_for_server
        self.__common_key_between_client = common_key_between_clients
        self.__nonce = get_nonce()
        self.__from_username = from_username
        self.__to_username = to_username

    @property
    def from_username(self) -> str:
        return self.__from_username

    @property
    def to_username(self) -> str:
        return self.__to_username

    def encrypt_content(self) -> None:
        cipher_to_server = AES.new(self.__common_key_for_server, AES.MODE_EAX, self.__nonce)
        cipher_to_client = AES.new(self.__common_key_between_client, AES.MODE_EAX, self.__nonce)

        encrypted_content = cipher_to_server.encrypt(cipher_to_client.encrypt(self.content))

        self.content = encrypted_content

    def send(self, connection: Connection, encrypt: bool = False):
        if encrypt:
            self.encrypt_content()

        self.__send_header(connection, len(self.content))

        connection.send_raw(self.content)

    def __send_header(self,
                      connection: Connection,
                      content_length: int) -> None:
        package_header = json.dumps({'type': self.package_type.value,
                                     'header': self.header.value,
                                     'from_username': self.__from_username,
                                     'to_username': self.__to_username,
                                     'content_length': str(content_length),
                                     'tag_length': 0})
        package_header_size = '{:010}'.format(len(package_header))

        connection.send_raw(package_header_size.encode())
        connection.send_raw(package_header.encode())

    def __str__(self):
        return f'Package(type={self.package_type},\n' \
               f'header={self.header},\n' \
               f'content={self.content},\n' \
               f'tag={self.tag},\n' \
               f'from_username={self.__from_username},\n' \
               f'to_username={self.__to_username})'
