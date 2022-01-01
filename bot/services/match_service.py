from uuid import uuid4

from repositories.match_repository import match_repository
from repositories.user_repository import user_repository


class MatchService:
    def __init__(self, repository=match_repository, user_repo=user_repository):
        self._repository = repository
        self._user_repository = user_repo

    def get_matches(self):
        return self._repository.find_all()

    def add_match(self):
        match_id = uuid4().hex
        self._repository.create(match_id)

        return match_id

    def get_single_match(self, match_id):
        return self._repository.find_by_id(match_id)

    def add_player_to_match(self, player_id, match_id):
        player = self._user_repository.find_by_id(player_id)
        match = self.get_single_match(match_id)
        self._repository.add_player_to_match(match, player)

    def get_match_players(self, match_id):
        match = self.get_single_match(match_id)
        return self._user_repository.find_players_of_match(match)


match_service = MatchService()
