import json
import logging

import customtkinter

from client.client_class import Client
from client.client_gui.chat import ChatWindow
from client.client_gui.chats_manager import ChatsManager
from net.package_classes.package_headers import PackageHeader
from utils.singleton_utils import singleton


@singleton
class ChatListWindow(customtkinter.CTk):
    def __init__(self):
        customtkinter.set_appearance_mode("dark")

        super().__init__()

        self.title("CryptoChat (Список чатов)")
        self.geometry(f"{300}x{300}")
        self.protocol('WM_DELETE_WINDOW', self.__on_closing)

        self.__title_label = customtkinter.CTkLabel(self,
                                                    text='Список чатов: ',
                                                    font=('Monospace', 18))

        self.__title_label.place(relx=0.5, rely=0.2, anchor='center', relwidth=0.8)

        self.__scrollable_chat_frame = customtkinter.CTkScrollableFrame(self)

        self.__scrollable_chat_frame.place(relx=0.5, rely=0.55, anchor='center', relwidth=1, relheight=0.5)

        self.__reload_chat_list_button = customtkinter.CTkButton(self,
                                                                 font=('Monospace', 14),
                                                                 text='Обновить список чатов',
                                                                 command=self.__on_chat_reload)
        self.__reload_chat_list_button.place(relx=0.5, rely=0.9, anchor='center', relwidth=0.8)

    def update_chats(self, usernames: list[str]):
        for widget in self.__scrollable_chat_frame.winfo_children():
            widget.destroy()

        for username in usernames:
            chat_button = customtkinter.CTkButton(self.__scrollable_chat_frame,
                                                  font=('Monospace', 14),
                                                  text=username,
                                                  command=self.__make_open_chat_action(username))
            chat_button.pack(pady=5)

    def __on_closing(self):
        client = Client()

        client.disconnect()

        self.destroy()


    def __make_open_chat_action(self, username: str):
        def method():
            self.__on_open_chat(username)

        return method

    @staticmethod
    def __on_chat_reload():
        Client().send_security_content_to_server(PackageHeader.GetUsersInLobby,
                                                 b'0')

    @staticmethod
    def __on_open_chat(username: str):
        client = Client()

        client.send_security_content_to_server(PackageHeader.GetCommonKeyForUser,
                                               json.dumps({'to_username': username}).encode())

        chats_manager = ChatsManager()

        chat_window = chats_manager.open_chat(username)

        chat_window.mainloop()
