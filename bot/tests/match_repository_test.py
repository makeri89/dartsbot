import unittest
from uuid import uuid4

from repositories.match_repository import MatchRepository
from repositories.user_repository import UserRepository
from db import get_database_connection, drop_tables, initialize_database


class TestMatchRepository(unittest.TestCase):
    def setUp(self):
        self.repository = MatchRepository(get_database_connection())
        self.user_repository = UserRepository(get_database_connection())
        drop_tables()
        initialize_database()
        
    def test_database_is_empty_at_first(self):
        self.assertEqual(len(self.repository.find_all()), 0)
        
    def test_database_has_one_match_after_adding_one_match(self):
        self.repository.create(uuid4().hex)
        self.assertEqual(len(self.repository.find_all()), 1)
        
    def test_match_can_be_searched_with_id(self):
        test_id = uuid4().hex
        self.repository.create(test_id)
        match = self.repository.find_by_id(test_id)
        self.assertEqual(match.id, test_id)
        
    def test_user_is_connected_to_match(self):
        test_user_id = uuid4().hex
        test_user_name = 'Test User'
        test_match_id = uuid4().hex
        self.user_repository.create_user(test_user_id, test_user_name)
        self.repository.create(test_match_id)
        match = self.repository.find_by_id(test_match_id)
        user = self.user_repository.find_by_id(test_user_id)
        self.repository.add_player_to_match(match, user)
        self.assertEqual(len(self.user_repository.find_players_of_match(match)), 1)
