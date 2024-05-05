from net.package_classes.package_headers import PackageHeader
from server.stages.abstract_stage_class import AbstractStage
from server.stages.first_connect_stage import FirstConnectStage
from server.stages.generate_pair_pq_stage import GeneratePairPgStage
from server.stages.get_common_key_for_user_stage import GetCommonKeyForUserStage
from server.stages.get_open_key_stage import GetOpenKeyStage
from server.stages.get_test_package_by_secure_server_communicate_stage import \
    GetTestPackageBySecureServerCommunicateStage
from server.stages.get_users_in_lobby_stage import GetUsersInLobbyStage
from server.stages.join_to_lobby_stage import JoinToLobbyStage


def get_stage(header: PackageHeader) -> AbstractStage:
    return {
        PackageHeader.FirstConnect: FirstConnectStage,
        PackageHeader.GetPairOfPQ: GeneratePairPgStage,
        PackageHeader.GetOpenKey: GetOpenKeyStage,
        PackageHeader.TestPackageForSecurityByServerCommunicate: GetTestPackageBySecureServerCommunicateStage,
        PackageHeader.JoinToLobby: JoinToLobbyStage,
        PackageHeader.GetUsersInLobby: GetUsersInLobbyStage,
        PackageHeader.GetCommonKeyForUser: GetCommonKeyForUserStage,
    }[header]()
