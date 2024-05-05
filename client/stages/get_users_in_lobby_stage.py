import json
import logging

from client.client_class import Client
from client.stages.abstract_client_stage_class import AbstractClientStage
from net.package_classes.package_class import Package


class GetUsersInLobbyStage(AbstractClientStage):
    def process_package(self, client: Client, package: Package) -> None:
        content = json.loads(package.content.decode())

        users_list = content['users']

        logging.info(f'Список пользователей: {users_list}')
