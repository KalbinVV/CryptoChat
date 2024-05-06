import customtkinter


class ChatWindow(customtkinter.CTk):
    def __init__(self, username: str):
        customtkinter.set_appearance_mode("dark")

        super().__init__()

        self.title(f'Чат с {username}')
        self.geometry(f"{500}x{500}")

        self.__title_label = customtkinter.CTkLabel(self,
                                                    text=f'Чат с {username}',
                                                    font=('Monospace', 18))

        self.__title_label.place(relx=0.5, rely=0.2, anchor='center', relwidth=0.8)

        self.__scrollable_chat_frame = customtkinter.CTkScrollableFrame(self)

        self.__scrollable_chat_frame.place(relx=0.5, rely=0.55, anchor='center', relwidth=1, relheight=0.6)

        self.__text_entry = customtkinter.CTkEntry(self,
                                                   font=('Monospace', 12),
                                                   corner_radius=0)

        self.__text_entry.place(relx=0, rely=0.9, relwidth=0.9)

        self.__send_message_button = customtkinter.CTkButton(self,
                                                             text='>',
                                                             font=('Monospace', 12),
                                                             corner_radius=0)

        self.__send_message_button.place(relx=0.9, rely=0.9, relwidth=0.1)
