from entities.user import User

from repositories.user_repository import user_repository
from repositories.average_repository import average_repository

class AverageService:
    def __init__(self, user_repo=user_repository, average_repo=average_repository):
        self._user_repository = user_repo
        self._average_repository = average_repo
        
    def add_average(self, player, average):
        self._average_repository.create(player, average)
        
    def get_averages(self):
        return self._average_repository.find_all()
        
    def get_user_average(self, user):
        result = self._average_repository.get_player_average(user)
        return result

average_service = AverageService()
