import json
import logging

from client.client_class import Client
from client.stages.abstract_client_stage_class import AbstractClientStage
from net.package_classes.package_class import Package


class GetSessionKeyByUserStage(AbstractClientStage):
    def process_package(self, client: Client, package: Package) -> None:
        logging.debug(package.content)

        content = json.loads(package.content.decode())

        if content['status']:
            from_username = content['from_username']
            session_key = content['session_key'].encode()

            client.update_session_key(from_username, session_key)

            logging.debug(f'Сессионный ключ для общения с {from_username}: {session_key}')
        else:
            logging.error(f'Не удалось получить общий ключ: {content["detail"]}')
