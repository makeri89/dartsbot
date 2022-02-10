from dateutil import parser
from datetime import datetime, timedelta

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

    def get_date_average(self, player_id, date):
        player = self._user_repository.find_by_id(player_id)
        isodate = date.isoformat()
        return self._repository.find_player_averages_by_date(player, isodate)

    def get_all_averages_by_date(self, player_id):
        player = self._user_repository.find_by_id(player_id)
        oldest_match = self._match_repository.find_oldest_match_by_player(
            player
        )
        result = []
        date_to_fetch = parser.parse(oldest_match.date)
        today = datetime.now()
        delta = timedelta(days=1)
        while date_to_fetch <= today:
            avg = self.get_date_average(player.id, date_to_fetch)
            result.append(avg)
            date_to_fetch += delta
        return result

    def get_player_highscore(self, player_id):
        player = self._user_repository.find_by_id(player_id)
        return self._repository.find_player_highscore(player)

    def get_date_highscore(self, player_id, date):
        player = self._user_repository.find_by_id(player_id)
        isodate = date.isoformat()
        return self._repository.find_player_highscores_by_date(player, isodate)

    def get_all_highscores_by_date(self, player_id):
        player = self._user_repository.find_by_id(player_id)
        oldest_match = self._match_repository.find_oldest_match_by_player(
            player
        )
        result = []
        date_to_fetch = parser.parse(oldest_match.date)
        today = datetime.now()
        delta = timedelta(days=1)
        while date_to_fetch <= today:
            avg = self.get_date_highscore(player.id, date_to_fetch)
            result.append(avg)
            date_to_fetch += delta
        return result

    def get_player_top_averages(self, player_id):
        player = self._user_repository.find_by_id(player_id)
        return self._repository.find_player_top_averages(player)
    
    def get_player_past_month_average(self, player_id):
        player = self._user_repository.find_by_id(player_id)
        return self._repository.find_player_past_month_average(player)


score_service = ScoreService()
