import logging

from Crypto.Cipher import AES

from client.client_class import Client
from client.stages.abstract_client_stage_class import AbstractClientStage
from net.package_classes.secure_package_for_clients_communication_class import SecurePackageForClientsCommunication
from utils.security_utils import get_nonce


class GetMessageFromUserStage(AbstractClientStage):
    def process_package(self, client: Client, package: SecurePackageForClientsCommunication) -> None:
        from_username = package.from_username

        logging.info(f'Попытка получить сообщение от {from_username}...')

        session_key = client.get_session_key_for_username(from_username)

        if session_key is None:
            logging.info(f'Попытка получить сообщение от неизвестного пользователя, выбрасываем пакет.')
            return

        nonce = get_nonce()

        server_key_decipher = AES.new(client.get_server_storage()['common_key'], AES.MODE_EAX, nonce)
        client_key_decipher = AES.new(session_key, AES.MODE_EAX, nonce)

        decrypted_message = client_key_decipher.decrypt(package.content)

        logging.info(f'Сообщение от {from_username}: {decrypted_message}')
