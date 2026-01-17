import click
from .database import add_server, delete_server, initialize_database

@click.group()
def cli():
    """A CLI for managing Hyperscout server configurations."""
    pass

@cli.command()
@click.option('--server-name', required=True, help='The name of the server.')
@click.option('--bot-token', required=True, help='The bot token for the server.')
@click.option('--destination-channel-id', required=True, help='The destination channel ID for the server.')
def set(server_name, bot_token, destination_channel_id):
    """Adds or updates a server configuration."""
    initialize_database()
    add_server(server_name, bot_token, destination_channel_id)
    click.echo(f"Server configuration for '{server_name}' has been set.")

@cli.command()
@click.option('--server-name', required=True, help='The name of the server to delete.')
def delete(server_name):
    """Deletes a server configuration."""
    initialize_database()
    delete_server(server_name)
    click.echo(f"Server configuration for '{server_name}' has been deleted.")

if __name__ == '__main__':
    cli()
