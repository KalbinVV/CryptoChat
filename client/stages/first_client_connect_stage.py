import logging

from client.client_class import Client
from client.stages.abstract_client_stage_class import AbstractClientStage
from net.package_classes.insecure_package_class import InsecurePackage
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader


class FirstClientConnectStage(AbstractClientStage):
    def process_package(self, client: Client, package: Package) -> None:
        logging.info(f'Сервер позволил подключиться, устанавливаем соединенное соединение.')

        client.send(InsecurePackage(header=PackageHeader.GetPairOfPQ,
                                    content=b'0'))
