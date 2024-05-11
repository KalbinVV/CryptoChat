import logging
import tkinter
from tkinter import filedialog
from typing import Optional

import customtkinter

from client.client_class import Client
from net.package_classes.package_headers import PackageHeader


class ChatWindow(customtkinter.CTk):
    def __init__(self, username: str):
        customtkinter.set_appearance_mode("dark")

        super().__init__()

        self.__username = username

        self.title(f'Чат с {username}')
        self.geometry(f"{500}x{500}")
        self.protocol('WM_DELETE_WINDOW', self.__on_closing)

        self.__title_label = customtkinter.CTkLabel(self,
                                                    text=f'Чат с {username}',
                                                    font=('Monospace', 18))

        self.__title_label.place(relx=0.5, rely=0.2, anchor='center', relwidth=0.8)

        self.__scrollable_chat_frame = customtkinter.CTkScrollableFrame(self)

        self.__scrollable_chat_frame.place(relx=0.5, rely=0.55, anchor='center', relwidth=1, relheight=0.6)

        self.__text_entry = customtkinter.CTkEntry(self,
                                                   font=('Monospace', 12),
                                                   corner_radius=0)

        self.__text_entry.bind('<Return>', self.__on_message_send)

        self.__text_entry.place(relx=0, rely=0.9, relwidth=0.8)

        self.__send_file_button = customtkinter.CTkButton(self,
                                                          text='#',
                                                          font=('Monospace', 12),
                                                          corner_radius=0,
                                                          command=self.__on_file_send)

        self.__send_message_button = customtkinter.CTkButton(self,
                                                             text='>',
                                                             font=('Monospace', 12),
                                                             corner_radius=0,
                                                             command=self.__on_message_send)

        self.__send_file_button.place(relx=0.9, rely=0.9, relwidth=0.1)
        self.__send_message_button.place(relx=0.8, rely=0.9, relwidth=0.1)

    def add_message(self, username: str, message: str) -> None:
        message_label = customtkinter.CTkLabel(self.__scrollable_chat_frame,
                                               text=f'{username}: {message}',
                                               font=('Monospace', 12))
        message_label.pack(pady=5)

    def __on_message_send(self, event: Optional[tkinter.Event] = None) -> None:
        logging.debug(f'Send message...')

        text = self.__text_entry.get()

        if len(text) == 0:
            return

        self.__text_entry.delete(0, 'end')

        client = Client()

        client.send_security_content_to_client(PackageHeader.SendMessageToUser,
                                               self.__username,
                                               text.encode())

        self.add_message(client.username, text)

    def __on_file_send(self):
        file = filedialog.askopenfile()

        client = Client()

        client.send_file_to_client(self.__username,
                                   file.name)

    def __on_closing(self) -> None:
        from client.client_gui.chats_manager import ChatsManager

        chats_manager = ChatsManager()

        chats_manager.remove_chat_window_from_manager(self.__username, self)

        self.destroy()
