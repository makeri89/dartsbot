import unittest
from uuid import uuid4

from repositories.match_repository import MatchRepository
from repositories.user_repository import UserRepository
from repositories.score_repository import ScoreRepository
from db import get_database_connection, drop_tables, initialize_database


class TestScoreRepository(unittest.TestCase):
    def setUp(self):
        self.match_repository = MatchRepository(get_database_connection())
        self.user_repository = UserRepository(get_database_connection())
        self.score_repository = ScoreRepository(get_database_connection())
        drop_tables()
        initialize_database()
        self.user_id = uuid4().hex
        self.user_repository.create_user(self.user_id, 'Test User')
        
    def test_database_is_empty_at_first(self):
        self.assertEqual(len(self.score_repository.find_all()), 0)
        
    def test_score_can_be_created(self):
        user = self.user_repository.find_by_id(self.user_id)
        match_id = uuid4().hex
        self.match_repository.create(match_id)
        match = self.match_repository.find_by_id(match_id)
        self.score_repository.create(
            player=user,
            match=match,
            average=50.0,
            darts_used=31,
            highscore=120
        )
        self.assertEqual(len(self.score_repository.find_all()), 1)