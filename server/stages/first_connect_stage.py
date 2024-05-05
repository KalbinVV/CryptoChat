import logging

from net.connection_class import Connection
from net.package_classes.insecure_package_class import InsecurePackage
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader
from server.stages.abstract_stage_class import AbstractStage


class FirstConnectStage(AbstractStage):
    def process(self, connection: Connection, package: Package):
        logging.info(f'{connection.address} соединение позволено!')

        connection.send_package(InsecurePackage(header=PackageHeader.FirstConnect,
                                                content=b'0'))
