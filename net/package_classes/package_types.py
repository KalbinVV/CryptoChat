import enum


class PackageType(enum.Enum):
    Insecure = 'Insecure'
    SecureCommunicateWithServer = 'SecureCommunicateWithServer'
    SecureCommunicateBetweenClients = 'SecureCommunicateBetweenClients'

    def is_secure(self):
        return not self == PackageType.Insecure
