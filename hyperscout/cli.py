import click
from .database import add_guild, delete_guild, initialize_database

@click.group()
def cli():
    """A CLI for managing Hyperscout guild configurations."""
    pass

@cli.command()
@click.option('--display-name', required=True, help='The display name for the guild.')
@click.option('--guild-id', required=True, help='The Discord Guild ID.')
@click.option('--destination-channel-id', required=True, help='The destination channel ID for the guild.')
def set(display_name, guild_id, destination_channel_id):
    """Adds or updates a guild configuration."""
    initialize_database()
    add_guild(display_name, guild_id, destination_channel_id)
    click.echo(f"Guild configuration for '{display_name}' has been set.")

@cli.command()
@click.option('--display-name', required=True, help='The display name of the guild to delete.')
def delete(display_name):
    """Deletes a guild configuration."""
    initialize_database()
    delete_guild(display_name)
    click.echo(f"Guild configuration for '{display_name}' has been deleted.")

if __name__ == '__main__':
    cli()
