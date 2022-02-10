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

    def find_player_averages_by_date(self, player, isodate):
        cursor = self._connection.cursor()

        result = cursor.execute(
            '''
            SELECT u.name, AVG(s.average) AS average, m.date
            FROM users u, scores s, matches m
            WHERE u.id=s.player_id AND u.id=:user_id
            AND m.id=s.match_id AND m.date=datetime(:date)
            ''',
            {'user_id': player.id, 'date': isodate}
        )

        return result.fetchone()

    def find_player_highscore(self, player):
        cursor = self._connection.cursor()

        result = cursor.execute(
            '''
            SELECT :player_name AS name, MAX(highscore) AS highscore
            FROM scores
            WHERE player_id=:player_id
            ''',
            {'player_id': player.id, 'player_name': player.name}
        )

        return result.fetchone()

    def find_player_highscores_by_date(self, player, isodate):
        cursor = self._connection.cursor()

        result = cursor.execute(
            '''
            SELECT u.name, MAX(highscore) AS highscore, m.date
            FROM users u, scores s, matches m
            WHERE u.id=s.player_id AND u.id=:user_id
            AND m.id=s.match_id AND m.date=datetime(:date)
            ''',
            {'user_id': player.id, 'date': isodate}
        )

        return result.fetchone()
    
    def find_player_top_averages(self, player):
        cursor = self._connection.cursor()
        
        result = cursor.execute(
            '''
            SELECT u.name, s.average AS average
            FROM users u, scores s
            WHERE u.id=s.player_id AND u.id=:user_id
            ORDER BY average DESC LIMIT 3
            ''',
            {'user_id': player.id}
        )
        
        return result.fetchall()
    
    def find_player_past_month_average(self, player):
        cursor = self._connection.cursor()
        
        result = cursor.execute(
            '''
            SELECT u.name, AVG(s.average) AS average
            FROM users u, scores s, matches m
            WHERE u.id=s.player_id AND u.id=:user_id
            AND s.match_id=m.id AND m.date >= date('now', '-30 days')
            ''',
            {'user_id': player.id}
        )
        
        return result.fetchone()


score_repository = ScoreRepository(get_database_connection())
