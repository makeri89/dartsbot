import os
import sqlite3

dirname = os.path.dirname(__file__)

connection = sqlite3.connect(
    os.path.join(dirname, 'data', 'database.sqlite'),
    check_same_thread=False
)
connection.row_factory = sqlite3.Row

def drop_tables():
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS matches')
    
    connection.commit()

def create_tables():
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS averages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id TEXT REFERENCES users,
            average REAL,
            date TEXT
        );
    ''')
    
    connection.commit()
    
def initialize_database():
    drop_tables()
    create_tables()
    
def get_database_connection():
    return connection

if __name__ == '__main__':
    initialize_database()