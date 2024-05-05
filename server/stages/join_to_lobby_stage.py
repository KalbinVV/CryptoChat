import json
import logging

from net.connection_class import Connection
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader
from server.stages.abstract_stage_class import AbstractStage


class JoinToLobbyStage(AbstractStage):
    def process(self, connection: Connection, package: Package):
        content = json.loads(package.content.decode())
        username = content['username']

        server = connection.storage['server']

        server.update_username(connection, username)

        logging.info(f'{connection.address} подключился как: {username}')

        content = json.dumps({'status': True,
                              'username': username}).encode()

        connection.send_secure_content_by_server_communicate(PackageHeader.JoinToLobby,
                                                             content,
                                                             connection.storage['common_key'])
