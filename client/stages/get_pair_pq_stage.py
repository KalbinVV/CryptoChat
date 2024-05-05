import json
import logging
import random

from client.client_class import Client
from client.stages.abstract_client_stage_class import AbstractClientStage
from net.package_classes.insecure_package_class import InsecurePackage
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader


class GetPairPqStage(AbstractClientStage):
    def process_package(self, client: Client, package: Package) -> None:
        content = json.loads(package.content.decode())

        p = content['p']
        q = content['q']

        logging.debug(f'Получены уникальные числа p: {p} и q: {q}')

        client.storage['p'] = p
        client.storage['q'] = q

        closed_key = random.randint(100000, 1000000)

        client.storage['closed_key'] = closed_key

        open_key = pow(q, closed_key, p)

        content = json.dumps({'open_key': open_key}).encode()

        client.send(InsecurePackage(header=PackageHeader.GetOpenKey,
                                    content=content))
