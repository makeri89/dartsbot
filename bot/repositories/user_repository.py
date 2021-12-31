from db import get_database_connection
from entities.user import User

def row_to_user(row):
    return User(row['id'], row['name']) if row else None

class UserRepository:
    def __init__(self, connection):
        self._connection = connection
        
    def find_all(self):
        cursor = self._connection.cursor()
        
        cursor.execute('SELECT * FROM users')
        
        result = cursor.fetchall()
        
        return list(map(row_to_user, result))
    
    def find_by_id(self, id):
        cursor = self._connection.cursor()
        
        cursor.execute(
            'SELECT * FROM users WHERE id=:id',
            {'id': id}
        )
        
        result = cursor.fetchone()
        
        return row_to_user(result)
    
    def find_by_name(self, name):
        cursor = self._connection.cursor()
        
        cursor.execute(
            'SELECT * FROM users WHERE name=:name',
            {'name': name}
        )
        
        result = cursor.fetchone()
        
        return row_to_user(result)
    
    def create_user(self, id, username):
        cursor = self._connection.cursor()
        
        cursor.execute(
            'INSERT INTO users (id, name) VALUES (:id, :username)',
            {'id': id, 'username': username}
        )
        
        self._connection.commit()
        
    def find_players_of_match(self, match):
        cursor = self._connection.cursor()
        
        result = cursor.execute(
            'SELECT u.id, u.name FROM users u, players_to_matches pm \
                WHERE u.id=pm.player_id AND pm.match_id=:match_id',
            {'match_id': match.id}
        )
        
        return list(map(row_to_user, result.fetchall()))

user_repository = UserRepository(get_database_connection())
