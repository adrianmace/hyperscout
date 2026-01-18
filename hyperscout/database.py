import aiosqlite as sqlite3
import os
from typing import List, Tuple, Optional

DATABASE_PATH = os.getenv('HYPERSCOUT_DATABASE_PATH', '/data/hyperscout.db')

async def initialize_database():
    """Initializes the database and creates the guilds table if it doesn't exist."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    async with sqlite3.connect(DATABASE_PATH) as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS guilds (
                id INTEGER PRIMARY KEY,
                guild_id TEXT NOT NULL UNIQUE,
                destination_channel_id TEXT NOT NULL,
                spam_protection_minutes INTEGER DEFAULT 5,
                delete_after_hours INTEGER DEFAULT 24
            )
        ''')
        await conn.commit()

async def migrate_schema():
    """Applies any necessary schema migrations."""
    async with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = await conn.execute('PRAGMA table_info(guilds)')
        columns = [row[1] for row in await cursor.fetchall()]
        if 'spam_protection_minutes' not in columns:
            await conn.execute('ALTER TABLE guilds ADD COLUMN spam_protection_minutes INTEGER DEFAULT 5')
        if 'delete_after_days' in columns and 'delete_after_hours' not in columns:
            await conn.execute('ALTER TABLE guilds ADD COLUMN delete_after_hours INTEGER DEFAULT 24')
            await conn.execute('UPDATE guilds SET delete_after_hours = delete_after_days * 24')
            await conn.execute('ALTER TABLE guilds DROP COLUMN delete_after_days')
        elif 'delete_after_hours' not in columns:
            await conn.execute('ALTER TABLE guilds ADD COLUMN delete_after_hours INTEGER DEFAULT 24')
        await conn.commit()

async def configure_guild(guild_id: str, destination_channel_id: str, spam_protection_minutes: int, delete_after_hours: int):
    """Adds or updates a guild configuration in the database."""
    async with sqlite3.connect(DATABASE_PATH) as conn:
        await conn.execute('''
            INSERT OR REPLACE INTO guilds (guild_id, destination_channel_id, spam_protection_minutes, delete_after_hours)
            VALUES (?, ?, ?, ?)
        ''', (guild_id, destination_channel_id, spam_protection_minutes, delete_after_hours))
        await conn.commit()

async def delete_guild(guild_id: str):
    """Deletes a guild configuration from the database."""
    async with sqlite3.connect(DATABASE_PATH) as conn:
        await conn.execute('DELETE FROM guilds WHERE guild_id = ?', (guild_id,))
        await conn.commit()

async def get_all_guilds() -> List[Tuple[str, str, int, int]]:
    """Retrieves all guild configurations from the database."""
    async with sqlite3.connect(DATABASE_PATH) as conn:
        async with conn.execute('SELECT guild_id, destination_channel_id, spam_protection_minutes, delete_after_hours FROM guilds') as cursor:
            return await cursor.fetchall()

async def get_guild_by_id(guild_id: int) -> Optional[Tuple[str, str, int, int]]:
    """Retrieves a single guild configuration by its ID."""
    async with sqlite3.connect(DATABASE_PATH) as conn:
        async with conn.execute('SELECT guild_id, destination_channel_id, spam_protection_minutes, delete_after_hours FROM guilds WHERE guild_id = ?', (str(guild_id),)) as cursor:
            return await cursor.fetchone()
