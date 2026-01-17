import sqlite3
import os
from typing import List, Tuple, Optional

DATABASE_PATH = os.getenv('HYPERSCOUT_DATABASE_PATH', '/data/hyperscout.db')

def initialize_database():
    """Initializes the database and creates the guilds table if it doesn't exist."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guilds (
            id INTEGER PRIMARY KEY,
            guild_id TEXT NOT NULL UNIQUE,
            destination_channel_id TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_guild(guild_id: str, destination_channel_id: str):
    """Adds or updates a guild configuration in the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO guilds (guild_id, destination_channel_id)
        VALUES (?, ?)
    ''', (guild_id, destination_channel_id))
    conn.commit()
    conn.close()

def delete_guild(guild_id: str):
    """Deletes a guild configuration from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM guilds WHERE guild_id = ?', (guild_id,))
    conn.commit()
    conn.close()

def get_all_guilds() -> List[Tuple[str, str]]:
    """Retrieves all guild configurations from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT guild_id, destination_channel_id FROM guilds')
    guilds = cursor.fetchall()
    conn.close()
    return guilds

def get_guild_by_id(guild_id: int) -> Optional[Tuple[str, str]]:
    """Retrieves a single guild configuration by its ID."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT guild_id, destination_channel_id FROM guilds WHERE guild_id = ?', (str(guild_id),))
    guild = cursor.fetchone()
    conn.close()
    return guild
