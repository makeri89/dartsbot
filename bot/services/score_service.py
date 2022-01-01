from repositories.score_repository import score_repository
from repositories.match_repository import match_repository
from repositories.user_repository import user_repository


class ScoreService:
    def __init__(self,
                 repository=score_repository,
                 match_repo=match_repository,
                 user_repo=user_repository):
        self._repository = repository
        self._match_repository = match_repo
        self._user_repository = user_repo

    def get_all_scores(self):
        return self._repository.find_all()

    def add_score(self, match_id, player_id, average, darts_used, highscore):
        player = self._user_repository.find_by_id(player_id)
        match = self._match_repository.find_by_id(match_id)
        self._repository.create(player, match, average, darts_used, highscore)

    def get_average(self, player_id):
        player = self._user_repository.find_by_id(player_id)
        return self._repository.find_player_averages(player)


score_service = ScoreService()
