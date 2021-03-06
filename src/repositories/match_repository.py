from db import get_database_connection
from entities.match import Match


def row_to_match(row):
    return Match(row['id'], row['date']) if row else None


class MatchRepository:
    def __init__(self, connection):
        self._connection = connection

        self._id = None

    def find_all(self):
        cursor = self._connection.cursor()

        result = cursor.execute('SELECT * FROM matches')

        return list(map(row_to_match, result.fetchall()))

    def create(self, id):
        cursor = self._connection.cursor()

        self._id = id
        cursor.execute(
            '''
            INSERT INTO matches (id, date)
            VALUES (:id, datetime('now','start of day'))
            ''',
            {'id': self._id}
        )

        self._connection.commit()

    def find_by_id(self, id):
        cursor = self._connection.cursor()

        result = cursor.execute(
            'SELECT * FROM matches WHERE id=:id',
            {'id': id}
        )

        return row_to_match(result.fetchone())

    def add_player_to_match(self, match, player):
        cursor = self._connection.cursor()

        cursor.execute(
            'INSERT INTO players_to_matches (player_id, match_id) VALUES (:player_id, :match_id)',
            {'player_id': player.id, 'match_id': match.id}
        )

        self._connection.commit()

    def find_oldest_match_by_player(self, player):
        cursor = self._connection.cursor()

        result = cursor.execute(
            '''
            SELECT m.id, m.date FROM matches m, scores s
            WHERE s.match_id=m.id AND s.player_id=:player_id
            ORDER BY m.date ASC LIMIT 1
            ''',
            {'player_id': player.id}
        )

        return row_to_match(result.fetchone())

    def find_matches_by_date(self, iso8601_date):
        cursor = self._connection.cursor()

        result = cursor.execute(
            'SELECT * FROM matches WHERE date=datetime(:date)',
            {'date': iso8601_date}
        )

        return list(map(row_to_match, result.fetchall()))


match_repository = MatchRepository(get_database_connection())
