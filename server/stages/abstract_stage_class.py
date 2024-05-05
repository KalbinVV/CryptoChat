import abc

from net.connection_class import Connection
from net.package_classes.package_class import Package


class AbstractStage(abc.ABC):
    @abc.abstractmethod
    def process(self, connection: Connection,
                package: Package):
        ...
