import threading

import customtkinter as customtkinter

from client.client_class import Client
from client.client_gui.chat_list import ChatListWindow


class InitApp(customtkinter.CTk):
    def __init__(self):
        customtkinter.set_appearance_mode("dark")

        super().__init__()

        self.title("CryptoChat")
        self.geometry(f"{300}x{300}")
        self.protocol('WM_DELETE_WINDOW', self.__on_closing)

        self.__title_label = customtkinter.CTkLabel(self,
                                                    text='CryptoChat',
                                                    font=('Monospace', 22))

        self.__title_label.place(relx=0.5, rely=0.09, anchor='center')

        self.__address_entry = customtkinter.CTkEntry(self,
                                                      font=('Monospace', 12))

        self.__address_label = customtkinter.CTkLabel(self,
                                                      text='Адрес:',
                                                      font=('Monospace', 18))

        self.__address_label.place(relx=0.5, rely=0.2, anchor='center')
        self.__address_entry.place(relx=0.5, rely=0.3, anchor='center', relwidth=0.8)

        self.__port_entry = customtkinter.CTkEntry(self,
                                                   font=('Monospace>', 12))
        self.__port_label = customtkinter.CTkLabel(self,
                                                   text='Порт:',
                                                   font=('Monospace', 18))

        self.__port_label.place(relx=0.5, rely=0.4, anchor='center')
        self.__port_entry.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8)

        self.__username_label = customtkinter.CTkLabel(self,
                                                       text='Имя пользователя: ',
                                                       font=('Monospace', 18))
        self.__username_entry = customtkinter.CTkEntry(self,
                                                       font=('Monospace', 12))

        self.__username_label.place(relx=0.5, rely=0.6, anchor='center')
        self.__username_entry.place(relx=0.5, rely=0.7, anchor='center', relwidth=0.8)

        self.__connect_button = customtkinter.CTkButton(self,
                                                        font=('Monospace', 20),
                                                        text='Подключить',
                                                        command=self.__on_connect_to_server)

        self.__connect_button.place(relx=0.5, rely=0.9, anchor='center', relwidth=0.8)

    def __on_closing(self):
        self.destroy()

    def __on_connect_to_server(self):
        address = self.__address_entry.get()
        port = int(self.__port_entry.get())
        username = self.__username_entry.get()

        client = Client()

        client_thread = threading.Thread(target=client.connect,
                                         args=(address, port, username))
        client_thread.start()

        self.destroy()

        chat_list_window = ChatListWindow()
        chat_list_window.mainloop()
