import json
import logging

from client.client_class import Client
from client.client_gui.chat_list import ChatListWindow
from client.stages.abstract_client_stage_class import AbstractClientStage
from net.package_classes.package_class import Package


class GetUsersInLobbyStage(AbstractClientStage):
    def process_package(self, client: Client, package: Package) -> None:
        content = json.loads(package.content.decode())

        users_list = content['users']

        users_list.remove(client.username)

        logging.info(f'Список пользователей: {users_list}')

        chat_list_window = ChatListWindow()
        chat_list_window.update_chats(users_list)
