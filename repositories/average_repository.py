from db import get_database_connection

class AverageRepository:
    def __init__(self, connection):
        self._connection = connection
        
    def find_all(self):
        cursor = self._connection.cursor()
        
        cursor.execute('SELECT * FROM averages')
        
        return cursor.fetchall()
    
    def create(self, player, average):
        cursor = self._connection.cursor()
        
        cursor.execute('''
            INSERT INTO averages (player_id, average, date) 
            VALUES (?, ?, datetime('now', 'localtime'))
        ''', (player.id, average))
        
        self._connection.commit()
        
    def get_player_average(self, player):
        cursor = self._connection.cursor()
        
        cursor.execute('''
            SELECT u.name, avg(a.average) 
            FROM users u LEFT JOIN averages a 
            ON u.id = a.player_id AND u.id = ?
        ''', (player.id,))
        
        return cursor.fetchone()
        
average_repository = AverageRepository(get_database_connection())
