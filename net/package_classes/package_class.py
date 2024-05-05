import abc
from typing import Optional

from net.package_classes.package_headers import PackageHeader
from net.package_classes.package_types import PackageType


class Package(abc.ABC):
    def __init__(self, package_type: PackageType,
                 header: PackageHeader,
                 content: str | bytes,
                 tag: Optional[bytes] = None):
        self.__package_type = package_type
        self.__header = header
        self.__content = content
        self.__tag = tag

    @property
    def package_type(self) -> PackageType:
        return self.__package_type

    @property
    def header(self) -> PackageHeader:
        return self.__header

    @property
    def content(self) -> str | bytes:
        return self.__content

    @content.setter
    def content(self, content: bytes):
        self.__content = content

    @property
    def tag(self) -> Optional[bytes]:
        return self.__tag

    @tag.setter
    def tag(self, tag: bytes) -> None:
        self.__tag = tag

    @abc.abstractmethod
    def send(self, connection, encrypt: bool = True) -> None:
        ...

    def __str__(self):
        return f'Package(type={self.__package_type},\n' \
               f'header={self.__header},\n' \
               f'content={self.__content},\n' \
               f'tag={self.__tag})'
