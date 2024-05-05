from net.package_classes.package_headers import PackageHeader
from net.package_classes.package_types import PackageType

class PackageBuilder:
    @staticmethod
    def from_header(header: dict[str, str],
                    content: bytes = b''):
        package_type = PackageType[header['type']]
        package_header = PackageHeader[header['header']]

        if package_type == PackageType.Insecure:
            from net.package_classes.insecure_package_class import InsecurePackage
            return InsecurePackage(package_header,
                                   content)
        elif package_type == PackageType.SecureCommunicateWithServer:
            from net.package_classes.secure_package_by_communicate_with_server_class \
                import SecurePackageByCommunicateWithServer

            return SecurePackageByCommunicateWithServer(package_header,
                                                        content,
                                                        None,
                                                        header['from_username'])
        elif package_type == PackageType.SecureCommunicateBetweenClients:
            from net.package_classes.secure_package_for_clients_communication_class import \
                SecurePackageForClientsCommunication

            return SecurePackageForClientsCommunication(package_header,
                                                        content,
                                                        header['from_username'],
                                                        header['to_username'])
