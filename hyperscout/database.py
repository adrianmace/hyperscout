import sqlite3
import os
from typing import List, Tuple

DATABASE_PATH = '/data/hyperscout.db'

def initialize_database():
    """Initializes the database and creates the servers table if it doesn't exist."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY,
            server_name TEXT NOT NULL UNIQUE,
            bot_token TEXT NOT NULL,
            destination_channel_id TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_server(server_name: str, bot_token: str, destination_channel_id: str):
    """Adds or updates a server configuration in the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO servers (server_name, bot_token, destination_channel_id)
        VALUES (?, ?, ?)
    ''', (server_name, bot_token, destination_channel_id))
    conn.commit()
    conn.close()

def delete_server(server_name: str):
    """Deletes a server configuration from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM servers WHERE server_name = ?', (server_name,))
    conn.commit()
    conn.close()

def get_all_servers() -> List[Tuple[str, str, str]]:
    """Retrieves all server configurations from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT server_name, bot_token, destination_channel_id FROM servers')
    servers = cursor.fetchall()
    conn.close()
    return servers
