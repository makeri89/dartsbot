import unittest
from uuid import uuid4

from repositories.user_repository import UserRepository
from db import get_database_connection, drop_tables, initialize_database


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        drop_tables()
        initialize_database()
        self.repository = UserRepository(get_database_connection())

    def test_database_is_empty_at_first(self):
        self.assertEqual(len(self.repository.find_all()), 0)

    def test_database_has_one_user_after_adding_one(self):
        test_id = uuid4().hex
        test_name = 'Test user'
        self.repository.create_user(test_id, test_name)
        self.assertEqual(len(self.repository.find_all()), 1)

    def test_created_user_has_correct_name(self):
        test_id = uuid4().hex
        test_name = 'username test'
        self.repository.create_user(test_id, test_name)
        user = self.repository.find_all()[-1]
        self.assertEqual(user.name, test_name)

    def test_user_can_be_found_with_id(self):
        test_id = uuid4().hex
        test_name = 'id test'
        self.repository.create_user(test_id, test_name)
        user = self.repository.find_by_id(test_id)
        self.assertEqual(user.name, test_name)
