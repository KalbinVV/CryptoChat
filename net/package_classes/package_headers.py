import enum


class PackageHeader(enum.Enum):
    FirstConnect = 'FirstConnect'
    Disconnected = 'Disconnected'
    GetPairOfPQ = 'GetPairOfPQ'
    GetOpenKey = 'GetOpenKey'
    TestPackageForSecurityByServerCommunicate = 'TestPackageForSecurityByServerCommunicate'
    JoinToLobby = 'JoinToLobby'
    GetUsersInLobby = 'GetUsersInLobby'
    GetCommonKeyForUser = 'GetCommonKeyForUser'
    SendMessageToUser = 'SendMessageToUser'
