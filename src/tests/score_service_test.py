import unittest
from uuid import uuid4

from services.score_service import ScoreService
from services.user_service import UserService
from services.match_service import MatchService

from db import drop_tables, initialize_database


class TestScoreService(unittest.TestCase):
    def setUp(self):
        self.service = ScoreService()
        self.user_service = UserService()
        self.match_service = MatchService()
        drop_tables()
        initialize_database()

    def test_database_is_empty_at_first(self):
        self.assertEqual(len(self.service.get_all_scores()), 0)

    def test_score_can_be_added(self):
        player_id = uuid4().hex
        self.user_service.create_user(player_id, 'Test User')
        match_id = self.match_service.add_match()
        self.service.add_score(match_id, player_id, 30.0, 40, 68)
        self.assertEqual(len(self.service.get_all_scores()), 1)

    def test_average_is_calculated_correctly(self):
        player_id = uuid4().hex
        self.user_service.create_user(player_id, 'Test User')
        match_id = self.match_service.add_match()
        self.service.add_score(match_id, player_id, 30.0, 40, 68)
        match_2_id = self.match_service.add_match()
        self.service.add_score(match_2_id, player_id, 40.0, 40, 68)
        average = self.service.get_average(player_id)
        self.assertAlmostEqual(average['average'], 35.0)

    def test_average_is_fetched_by_date_correctly(self):
        player_id = uuid4().hex
        self.user_service.create_user(player_id, 'Test User')
        match_id = self.match_service.add_match()
        self.service.add_score(match_id, player_id, 30.0, 40, 68)
        result = self.service.get_all_averages_by_date(player_id)
        self.assertAlmostEqual(result[0]['average'], 30.0)

    def test_highscore_is_fetched_correctly_by_player_id(self):
        player_id = uuid4().hex
        self.user_service.create_user(player_id, 'Test User')
        match_id = self.match_service.add_match()
        self.service.add_score(match_id, player_id, 30.0, 40, 68)
        match_2_id = self.match_service.add_match()
        self.service.add_score(match_2_id, player_id, 30.0, 40, 24)
        result = self.service.get_player_highscore(player_id)
        self.assertEqual(result['highscore'], 68)
        self.assertListEqual(result.keys(), ['name', 'highscore'])
