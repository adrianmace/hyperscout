import click
from .database import add_guild, delete_guild, initialize_database

@click.group()
def cli():
    """A CLI for managing Hyperscout guild configurations."""
    pass

@cli.command()
@click.option('--guild-id', required=True, help='The Discord Guild ID.')
@click.option('--destination-channel-id', required=True, help='The destination channel ID for the guild.')
def set(guild_id, destination_channel_id):
    """Adds or updates a guild configuration."""
    initialize_database()
    add_guild(guild_id, destination_channel_id)
    click.echo(f"Guild configuration for guild '{guild_id}' has been set.")

@cli.command()
@click.option('--guild-id', required=True, help='The guild ID of the guild to delete.')
def delete(guild_id):
    """Deletes a guild configuration."""
    initialize_database()
    delete_guild(guild_id)
    click.echo(f"Guild configuration for guild '{guild_id}' has been deleted.")

if __name__ == '__main__':
    cli()
