import json
import logging
from typing import Optional

from Crypto.Cipher import AES

from net.connection_class import Connection
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader
from net.package_classes.package_types import PackageType
from utils.security_utils import get_nonce


class SecurePackageByCommunicateWithServer(Package):
    def __init__(self, header: PackageHeader,
                 content: bytes,
                 common_key: Optional[bytes] = None,
                 from_username: Optional[str] = None):
        super().__init__(PackageType.SecureCommunicateWithServer,
                         header,
                         content,
                         tag=None)

        self.__common_key = common_key
        self.__nonce = get_nonce()
        self.__from_username = from_username

    def encrypt_content(self) -> None:
        cipher = AES.new(self.__common_key, AES.MODE_EAX, self.__nonce)

        encrypted_content, tag = cipher.encrypt_and_digest(self.content)

        self.tag = tag
        self.content = encrypted_content

    def send(self, connection: Connection, encrypt: bool = True):
        if encrypt:
            self.encrypt_content()

        self.__send_header(connection, len(self.content))

        connection.send_raw(self.tag)
        connection.send_raw(self.content)

    def __send_header(self,
                      connection: Connection,
                      content_length: int) -> None:
        package_header = json.dumps({'type': self.package_type.value,
                                     'header': self.header.value,
                                     'content_length': str(content_length),
                                     'tag_length': len(self.tag),
                                     'from_username': self.__from_username})
        package_header_size = '{:010}'.format(len(package_header))

        connection.send_raw(package_header_size.encode())
        connection.send_raw(package_header.encode())

    @property
    def from_username(self):
        return self.__from_username

    def __str__(self):
        return f'Package(type={self.package_type},\n' \
               f'header={self.header},\n' \
               f'content={self.content},\n' \
               f'tag={self.tag},\n' \
               f'from_username={self.__from_username})'
