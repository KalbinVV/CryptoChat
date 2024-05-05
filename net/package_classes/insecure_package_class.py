import json

from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader
from net.package_classes.package_types import PackageType
from net.connection_class import Connection


class InsecurePackage(Package):

    def __init__(self, header: PackageHeader, content: bytes):
        super().__init__(package_type=PackageType.Insecure,
                         header=header,
                         content=content)

        self.__content = content

    def send(self, connection: Connection, encrypt: bool = False):
        self.__send_header(connection, len(self.content))
        connection.send_raw(self.content)

    def __send_header(self,
                      connection: Connection,
                      content_length: int) -> None:
        package_header = json.dumps({'type': self.package_type.value,
                                     'header': self.header.value,
                                     'content_length': str(content_length)})
        package_header_size = '{:010}'.format(len(package_header))

        connection.send_raw(package_header_size.encode())
        connection.send_raw(package_header.encode())