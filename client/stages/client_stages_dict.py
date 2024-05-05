from client.stages.abstract_client_stage_class import AbstractClientStage
from client.stages.first_client_connect_stage import FirstClientConnectStage
from client.stages.get_message_from_user_stage import GetMessageFromUserStage
from client.stages.get_open_key_stage import GetOpenKeyStage
from client.stages.get_pair_pq_stage import GetPairPqStage
from client.stages.get_session_key_by_user_stage import GetSessionKeyByUserStage
from client.stages.get_users_in_lobby_stage import GetUsersInLobbyStage
from client.stages.join_to_lobby_stage import JoinToLobbyStage
from net.package_classes.package_headers import PackageHeader


def get_stage(header: PackageHeader) -> AbstractClientStage:
    return {
        PackageHeader.FirstConnect: FirstClientConnectStage,
        PackageHeader.GetPairOfPQ: GetPairPqStage,
        PackageHeader.GetOpenKey: GetOpenKeyStage,
        PackageHeader.GetUsersInLobby: GetUsersInLobbyStage,
        PackageHeader.JoinToLobby: JoinToLobbyStage,
        PackageHeader.GetCommonKeyForUser: GetSessionKeyByUserStage,
        PackageHeader.SendMessageToUser: GetMessageFromUserStage
    }[header]()
