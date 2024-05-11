import pickle
from pathlib import Path

from net.package_classes.package_headers import PackageHeader
from net.package_classes.secure_package_for_clients_communication_class import SecurePackageForClientsCommunication

from typing import Optional


class FilePackage(SecurePackageForClientsCommunication):
    def __init__(self,
                 file_path: str,
                 from_username: str,
                 to_username: str,
                 common_key_for_server: Optional[bytes] = None,
                 common_key_between_clients: Optional[bytes] = None
                 ):
        with open(file_path, 'rb') as f:
            file_binary = f.read()

        content = {'file_name': Path(file_path).name,
                   'binary_content': file_binary}

        super().__init__(PackageHeader.SendFileToUser,
                         pickle.dumps(content),
                         from_username,
                         to_username,
                         common_key_for_server,
                         common_key_between_clients)
