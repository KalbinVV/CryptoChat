import json
import logging

from client.client_class import Client
from client.stages.abstract_client_stage_class import AbstractClientStage
from net.package_classes.package_class import Package
from utils.security_utils import get_random_session_key


class JoinToLobbyStage(AbstractClientStage):
    def process_package(self, client: Client, package: Package) -> None:
        content = json.loads(package.content.decode())
        status = content['status']

        if not status:
            logging.error(f'Не удалось зайти в лобби с данным именем!')
        else:
            username = content['username']

            logging.info(f'Вы успешно вошли в лобби как: {username}!')

            client.update_username(username)
