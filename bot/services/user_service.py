from repositories.user_repository import user_repository


class UserService:
    def __init__(self, repository=user_repository):
        self._repository = repository

    def create_user(self, id, name):
        self._repository.create_user(id, name)

    def get_users(self):
        return self._repository.find_all()

    def get_user_by_id(self, id):
        return self._repository.find_by_id(id)

    def get_user_by_name(self, name):
        return self._repository.find_by_name(name)


user_service = UserService()
