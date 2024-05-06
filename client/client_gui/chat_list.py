import customtkinter

from utils.singleton_utils import singleton


@singleton
class ChatListWindow(customtkinter.CTk):
    def __init__(self):
        customtkinter.set_appearance_mode("dark")

        super().__init__()

        self.title("CryptoChat (Список чатов)")
        self.geometry(f"{300}x{300}")

        self.__title_label = customtkinter.CTkLabel(self,
                                                    text='Список чатов: ',
                                                    font=('Monospace', 18))

        self.__title_label.place(relx=0.5, rely=0.2, anchor='center', relwidth=0.8)

        self.__scrollable_chat_frame = customtkinter.CTkScrollableFrame(self)

        self.__scrollable_chat_frame.place(relx=0.5, rely=0.55, anchor='center', relwidth=1, relheight=0.5)

        self.__reload_chat_list_button = customtkinter.CTkButton(self,
                                                                 font=('Monospace', 14),
                                                                 text='Обновить список чатов')
        self.__reload_chat_list_button.place(relx=0.5, rely=0.9, anchor='center', relwidth=0.8)
