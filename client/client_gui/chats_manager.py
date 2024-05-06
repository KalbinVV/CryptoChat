import logging
import threading

from client.client_gui.chat import ChatWindow
from utils.singleton_utils import singleton


@singleton
class ChatsManager:
    def __init__(self):
        self.__chats_dict: dict[str, list[ChatWindow]] = dict()

    def add_chat_window_to_manager(self, username: str, chat_window: ChatWindow):
        logging.debug(f'Chat {chat_window} binded to {username}')

        chats_dict_list = self.__chats_dict.setdefault(username, list())
        chats_dict_list.append(chat_window)

    def remove_chat_window_from_manager(self, username: str, chat_window: ChatWindow):
        logging.debug(f'Chat {chat_window} unbinded from {username}')

        chats_dict_list = self.__chats_dict.setdefault(username, list())

        chats_dict_list.remove(chat_window)

    def remove_all_chat_windows_from_manager(self, username: str):
        del self.__chats_dict[username]

    def add_message_to_all_chats(self, username: str, message: str):
        chats_dict_list = self.__chats_dict.setdefault(username, list())

        def start_window_in_another_thread():
            new_chat_window = self.open_chat(username)
            new_chat_window.add_message(username, message)
            new_chat_window.mainloop()

        if len(chats_dict_list) == 0:
            new_chat_window_thread = threading.Thread(target=start_window_in_another_thread,
                                                      daemon=True)
            new_chat_window_thread.start()

            return

        for chat_window in chats_dict_list:
            chat_window.add_message(username, message)

    def open_chat(self, username: str) -> ChatWindow:
        chat_window = ChatWindow(username)

        self.add_chat_window_to_manager(username, chat_window)

        return chat_window
