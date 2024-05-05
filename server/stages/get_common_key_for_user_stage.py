import json
import logging

from net.connection_class import Connection
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader
from server.stages.abstract_stage_class import AbstractStage
from utils.security_utils import get_random_session_key


class GetCommonKeyForUserStage(AbstractStage):
    def process(self, connection: Connection, package: Package):
        content = json.loads(package.content.decode())

        to_username = content['to_username']
        server = connection.storage['server']

        logging.info(f'{connection.address} запрос общий ключ для {to_username}')

        to_connection = server.get_connection_by_username(to_username)
        from_username = server.get_username_by_connection(connection)

        if to_connection is None or from_username is None:
            content = json.dumps({'status': False,
                                  'detail': 'Username not exists or you don"t join to lobby!'}).encode()

            connection.send_secure_content_by_server_communicate(PackageHeader.GetCommonKeyForUser,
                                                                 content,
                                                                 connection.storage['common_key'])
        else:
            session_key = get_random_session_key(length=32)

            logging.debug(f'Общий ключ между {from_username} и {to_username}: {session_key}')

            content = {'status': True,
                       'from_username': to_username,
                       'to_username': from_username,
                       'session_key': session_key.decode()}

            connection.send_secure_content_by_server_communicate(PackageHeader.GetCommonKeyForUser,
                                                                 json.dumps(content).encode(),
                                                                 connection.storage['common_key'])

            content['from_username'] = from_username
            content['to_username'] = to_username

            from net.package_classes.insecure_package_class import InsecurePackage
            to_connection.send_package(InsecurePackage(PackageHeader.GetCommonKeyForUser,
                                                       json.dumps(content).encode()))
