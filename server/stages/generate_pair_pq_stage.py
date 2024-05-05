import json

from net.connection_class import Connection
from net.package_classes.package_class import Package
from net.package_classes.package_headers import PackageHeader

from server.stages.abstract_stage_class import AbstractStage
from utils.generator_utls import get_random_prime
from utils.math_utils import find_primitive_root


class GeneratePairPgStage(AbstractStage):
    MIN_PRIME_NUMBER = 10000
    MAX_PRIME_NUMBER = 100000

    def process(self, connection: Connection, package: Package):
        p = get_random_prime(self.MIN_PRIME_NUMBER, self.MAX_PRIME_NUMBER)
        q = find_primitive_root(p)

        connection.storage['p'] = p
        connection.storage['q'] = q

        content = json.dumps({'p': p,
                              'q': q}).encode()

        from net.package_classes.insecure_package_class import InsecurePackage
        connection.send_package(InsecurePackage(header=PackageHeader.GetPairOfPQ,
                                                content=content))
