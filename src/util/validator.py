from repositories.user_repository import user_repository


class Validator:
    def __init__(self):
        pass

    def validate_user_creation(self, id, username):
        id_validation = self.validate_id(id)
        if id_validation != 'valid':
            return id_validation
        name_validation = self.validate_username(username)
        return name_validation

    def validate_username(self, username):
        if not self._check_length(username):
            return 'username too short'
        if self._username_exists(username):
            return 'username already exists'
        return 'valid'

    def validate_id(self, id):
        if self._id_exists(id):
            return 'you are already registered'
        return 'valid'

    def _check_length(self, username):
        return 3 <= len(username)

    def _username_exists(self, username):
        user = user_repository.find_by_name(username)
        return user is not None

    def _id_exists(self, id):
        user = user_repository.find_by_id(id)
        return user is not None
