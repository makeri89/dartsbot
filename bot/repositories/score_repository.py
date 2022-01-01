from db import get_database_connection


class ScoreRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()

        result = cursor.execute('SELECT * FROM scores')

        return result.fetchall()

    def create(self, player, match, average, darts_used, highscore):
        cursor = self._connection.cursor()

        cursor.execute(
            '''
            INSERT INTO scores
            (player_id, match_id, average, darts_used, highscore)
            VALUES
            (:player_id, :match_id, :average, :darts_used, :highscore)
            ''',
            {
                'player_id': player.id, 'match_id': match.id,
                'average': average, 'darts_used': darts_used,
                'highscore': highscore
            }
        )

        self._connection.commit()

    def find_player_averages(self, player):
        cursor = self._connection.cursor()

        result = cursor.execute(
            '''
            SELECT u.name, AVG(s.average) AS average
            FROM users u, scores s
            WHERE u.id=s.player_id AND u.id=:user_id
            ''',
            {'user_id': player.id}
        )

        return result.fetchone()


score_repository = ScoreRepository(get_database_connection())
