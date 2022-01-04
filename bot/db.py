import os
import sqlite3

from config import DATABASE_URL

dirname = os.path.dirname(__file__)

connection = sqlite3.connect(
    os.path.join(dirname, '..', 'data', DATABASE_URL),
    check_same_thread=False
)
connection.row_factory = sqlite3.Row


def drop_tables():
    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS averages')
    cursor.execute('DROP TABLE IF EXISTS player_to_matches')
    cursor.execute('DROP TABLE IF EXISTS matches')
    cursor.execute('DROP TABLE IF EXISTS scores')

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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id TEXT PRIMARY KEY,
            date TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            player_id TEXT REFERENCES users,
            match_id TEXT REFERENCES matches,
            average REAL,
            darts_used INTEGER,
            highscore INTEGER
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players_to_matches (
            player_id TEXT REFERENCES users,
            match_id TEXT REFERENCES matches
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
