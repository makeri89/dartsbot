import unittest

from util.validator import Validator
from repositories.user_repository import user_repository
from db import initialize_database


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = Validator()
        initialize_database()

    def test_too_short_username_does_not_pass_validator(self):
        username = 'aa'
        validation = self.validator.validate_username(username)
        self.assertEqual(validation, 'username too short')

    def test_username_that_already_exists_does_not_pass_validator(self):
        user_id = '12345'
        username = 'aaaa'
        user_repository.create_user(user_id, username)
        validation = self.validator.validate_username(username)
        self.assertEqual(validation, 'username already exists')

    def test_valid_username_passes_validator(self):
        user_repository.create_user('12345', 'aaaaa')
        validation = self.validator.validate_username('bbbbb')
        self.assertEqual(validation, 'valid')

    def test_existing_id_does_not_pass_validator(self):
        user_id = '12345'
        username = 'aaaa'
        user_repository.create_user(user_id, username)
        validation = self.validator.validate_id(user_id)
        self.assertEqual(validation, 'you are already registered')

    def test_nonexisting_id_passes_validator(self):
        user_id = '12345'
        username = 'aaaa'
        user_repository.create_user(user_id, username)
        validation = self.validator.validate_id('23456')
        self.assertEqual(validation, 'valid')
