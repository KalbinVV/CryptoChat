import json
import logging

from net.connection_class import Connection
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader
from server.stages.abstract_stage_class import AbstractStage


class GetUsersInLobbyStage(AbstractStage):
    def process(self, connection: Connection, package: Package):
        logging.info(f'{connection.address} запрос список пользователей')

        server = connection.storage['server']
        users = server.get_users_in_lobby()
        common_key = connection.storage['common_key']

        content = json.dumps({'users': users}).encode()

        connection.send_secure_content_by_server_communicate(PackageHeader.GetUsersInLobby,
                                                             content,
                                                             common_key)
