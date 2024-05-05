import logging

from net.connection_class import Connection
from net.package_classes.package_class import Package
from server.stages.abstract_stage_class import AbstractStage


class GetTestPackageBySecureServerCommunicateStage(AbstractStage):
    def process(self, connection: Connection, package: Package):
        content = package.content.decode()

        logging.info(f'Получен тестовый пакет для проверки защищенного соединения с сервером, сообщение: {content}')
