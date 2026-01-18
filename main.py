import os
import sys
import asyncio
import discord
import logging

from hyperscout.database import initialize_database, migrate_schema
from hyperscout.bot import HyperscoutBot
from hyperscout.cli import cli
from hyperscout.logging_config import setup_logging

# Configure logging
setup_logging()

async def start_bot():
    """
    Initializes the database and runs the single bot client.
    """
    await initialize_database()
    await migrate_schema()

    bot_token = os.getenv('HYPERSCOUT_BOT_TOKEN')
    if not bot_token:
        logging.error(
            "HYPERSCOUT_BOT_TOKEN environment variable not set.",
            extra={"event": "startup_error", "error_code": "missing_token"}
        )
        sys.exit(1)

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    intents.voice_states = True
    intents.guilds = True

    bot = HyperscoutBot(command_prefix='!', intents=intents)

    # Load cogs
    for filename in os.listdir('./hyperscout/cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            await bot.load_extension(f'hyperscout.cogs.{filename[:-3]}')

    try:
        logging.info("Starting Hyperscout...", extra={"event": "startup"})
        await bot.start(bot_token)
    except discord.errors.LoginFailure:
        logging.error(
            "Failed to log in. Please check the HYPERSCOUT_BOT_TOKEN.",
            extra={"event": "login_failure"}
        )
    except Exception as e:
        logging.error(
            "An unexpected error occurred.",
            extra={"event": "unexpected_error", "error": str(e)}
        )
    finally:
        if not bot.is_closed():
            await bot.close()
        logging.info("Hyperscout has been shut down.", extra={"event": "shutdown"})

def main():
    # If there are command-line arguments, assume it's a CLI command.
    if len(sys.argv) > 1:
        cli()
    else:
        try:
            asyncio.run(start_bot())
        except KeyboardInterrupt:
            logging.info("Shutting down Hyperscout.", extra={"event": "shutdown_request"})

if __name__ == "__main__":
    main()
