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

    def test_all_time_averages_are_found_correctly(self):
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
        match_2_id = uuid4().hex
        self.match_repository.create(match_2_id)
        match_2 = self.match_repository.find_by_id(match_2_id)
        self.score_repository.create(
            player=user,
            match=match_2,
            average=40.0,
            darts_used=31,
            highscore=120
        )
        self.assertAlmostEqual(
            self.score_repository.find_player_averages(user)['average'], 45.0)

    def test_average_by_date_returns_none_with_date_that_has_no_scores(self):
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
        date = '2020-01-01 00:00:00'
        result = self.score_repository.find_player_averages_by_date(user, date)
        self.assertEqual(result['average'], None)

    def test_highscore_is_fetched_correctly(self):
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
        match_2_id = uuid4().hex
        self.match_repository.create(match_2_id)
        match = self.match_repository.find_by_id(match_2_id)
        self.score_repository.create(
            player=user,
            match=match,
            average=50.0,
            darts_used=31,
            highscore=40
        )

        result = self.score_repository.find_player_highscore(user)
        self.assertEqual(result['highscore'], 120)
        self.assertEqual(result['name'], 'Test User')
