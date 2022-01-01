import unittest
from uuid import uuid4

from db import drop_tables, initialize_database
from services.match_service import MatchService
from services.user_service import user_service


class TestMatchService(unittest.TestCase):
    def setUp(self):
        self.service = MatchService()
        self.user_service = user_service
        drop_tables()
        initialize_database()

    def test_database_is_empty_at_first(self):
        self.assertEqual(len(self.service.get_matches()), 0)

    def test_one_match_is_created_correctly(self):
        self.service.add_match()
        self.assertEqual(len(self.service.get_matches()), 1)

    def test_match_is_found_with_id(self):
        match_id = self.service.add_match()
        match = self.service.get_single_match(match_id)
        self.assertEqual(match.id, match_id)

    def test_player_can_be_added_to_match(self):
        match_id = self.service.add_match()
        player_id = uuid4().hex
        player_name = 'Test User'
        self.user_service.create_user(player_id, player_name)
        self.service.add_player_to_match(player_id, match_id)
        result = self.service.get_match_players(match_id)
        self.assertEqual(len(result), 1)
