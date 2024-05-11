import logging
import pickle
from tkinter import filedialog

from Crypto.Cipher import AES

from client.client_class import Client
from client.stages.abstract_client_stage_class import AbstractClientStage
from net.package_classes.file_package import FilePackage
from utils.security_utils import get_nonce


class GetFileStage(AbstractClientStage):
    def process_package(self, client: Client, package: FilePackage) -> None:
        from_username = package.from_username

        logging.info(f'Попытка получить файл от {from_username}...')

        session_key = client.get_session_key_for_username(from_username)

        if session_key is None:
            logging.info(f'Попытка получить файл от неизвестного пользователя, выбрасываем пакет.')
            return

        nonce = get_nonce()

        client_key_decipher = AES.new(session_key, AES.MODE_EAX, nonce)

        decrypted_content = client_key_decipher.decrypt(package.content)

        content = pickle.loads(decrypted_content)

        file_name = content['file_name']
        file_binary = content['binary_content']

        file_path = filedialog.asksaveasfilename(initialfile=file_name)

        with open(file_path, 'wb') as f:
            f.write(file_binary)
