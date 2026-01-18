import click
import asyncio
from .database import configure_guild, delete_guild, initialize_database

@click.group()
def cli():
    """A CLI for managing Hyperscout guild configurations."""
    pass

@cli.command()
@click.option('--guild-id', required=True, help='The Discord Guild ID.')
@click.option('--destination-channel-id', required=True, help='The destination channel ID for the guild.')
def set(guild_id, destination_channel_id):
    """Adds or updates a guild configuration."""
    async def main():
        await initialize_database()
        await configure_guild(guild_id, destination_channel_id)
        click.echo(f"Guild configuration for guild '{guild_id}' has been set.")
    asyncio.run(main())

@cli.command()
@click.option('--guild-id', required=True, help='The guild ID of the guild to delete.')
def delete(guild_id):
    """Deletes a guild configuration."""
    async def main():
        await initialize_database()
        await delete_guild(guild_id)
        click.echo(f"Guild configuration for guild '{guild_id}' has been deleted.")
    asyncio.run(main())

if __name__ == '__main__':
    cli()
