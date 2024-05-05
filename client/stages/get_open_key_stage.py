import json
import logging

from client.client_class import Client
from client.stages.abstract_client_stage_class import AbstractClientStage
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader
from utils.security_utils import generate_common_key


class GetOpenKeyStage(AbstractClientStage):
    def process_package(self, client: Client, package: Package) -> None:
        content = json.loads(package.content.decode())

        p = client.storage['p']

        server_open_key = content['open_key']

        common_seed_key = pow(server_open_key, client.storage['closed_key'], p)

        logging.debug(f'Общий зерно сеансового ключ: {common_seed_key}')

        common_key = generate_common_key(common_seed_key, length=32)

        logging.debug(f'Общий сеансовый ключ: {common_key}')

        client.get_server_storage()['common_key'] = common_key

        logging.info(f'Безопасное соединение установлено!')

        client.send_security_content_to_server(PackageHeader.TestPackageForSecurityByServerCommunicate,
                                               b'Hello, server!')

        del client.storage['p']
        del client.storage['q']
        del client.storage['closed_key']
