import json
import logging
import random

from net.connection_class import Connection
from net.package_classes.insecure_package_class import InsecurePackage
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader
from server.stages.abstract_stage_class import AbstractStage
from utils.security_utils import generate_common_key


class GetOpenKeyStage(AbstractStage):
    def process(self, connection: Connection, package: Package):
        content = json.loads(package.content.decode())

        p = connection.storage['p']
        q = connection.storage['q']

        closed_key = random.randint(100000, 1000000)
        open_key = pow(q, closed_key, p)

        client_open_key = content['open_key']

        common_seed_key = pow(client_open_key, closed_key, p)

        logging.debug(f'Общее зерно для сеансового ключа {connection.address}: {common_seed_key}')

        common_key = generate_common_key(common_seed_key, length=32)

        logging.debug(f'Общий сеансовый ключ для {connection.address}: {common_key}')

        connection.storage['common_key'] = common_key

        content = json.dumps({'open_key': open_key}).encode()

        del connection.storage['p']
        del connection.storage['q']

        connection.send_package(InsecurePackage(header=PackageHeader.GetOpenKey,
                                                content=content))

        logging.info(f'Безопасное соединение с {connection.address} установлено.')

