from repositories.user_repository import user_repository
from util.validator import Validator


class UserService:
    def __init__(self, repository=user_repository):
        self._repository = repository
        self._validator = Validator()

    def create_user(self, id, name):
        validation = self._validator.validate_user_creation(id, name)
        if validation == 'valid':
            self._repository.create_user(id, name)
        return validation

    def get_users(self):
        return self._repository.find_all()

    def get_user_by_id(self, id):
        return self._repository.find_by_id(id)

    def get_user_by_name(self, name):
        return self._repository.find_by_name(name)


user_service = UserService()
