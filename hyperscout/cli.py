import click
import asyncio
import os
import discord
import logging

from .bot import HyperscoutBot
from .database import configure_guild, delete_guild, initialize_database
from .cogs.purge import purge_bot_messages

logger = logging.getLogger(__name__)

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

@cli.command()
def purge():
    """Triggers a manual purge of bot messages."""
    async def main():
        await initialize_database()

        bot_token = os.getenv('HYPERSCOUT_BOT_TOKEN')
        if not bot_token:
            logger.error(
                "HYPERSCOUT_BOT_TOKEN environment variable not set.",
                extra={"event": "startup_error", "error_code": "missing_token"}
            )
            return

        intents = discord.Intents.default()
        bot = HyperscoutBot(command_prefix='!', intents=intents)

        @bot.event
        async def on_ready():
            click.echo("Bot logged in, starting purge...")
            await purge_bot_messages(bot)
            await bot.close()
            click.echo("Purge complete.")

        try:
            await bot.start(bot_token)
        except discord.errors.LoginFailure:
            logger.error(
                "Failed to log in. Please check the HYPERSCOUT_BOT_TOKEN.",
                extra={"event": "login_failure"}
            )

    click.echo("Starting manual purge... logging in bot.")
    asyncio.run(main())

if __name__ == '__main__':
    cli()
