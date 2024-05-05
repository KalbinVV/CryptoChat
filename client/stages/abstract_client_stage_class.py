import abc

from client.client_class import Client
from net.package_classes.package_class import Package


class AbstractClientStage(abc.ABC):
    @abc.abstractmethod
    def process_package(self, client: Client, package: Package) -> None:
        ...
