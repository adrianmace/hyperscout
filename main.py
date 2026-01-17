import os
import sys
import asyncio
import discord
import logging

from hyperscout.database import initialize_database
from hyperscout.bot import HyperscoutBot
from hyperscout.cli import cli

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def start_bot():
    """
    Initializes the database and runs the single bot client.
    """
    initialize_database()

    bot_token = os.getenv('HYPERSCOUT_BOT_TOKEN')
    if not bot_token:
        logging.error("HYPERSCOUT_BOT_TOKEN environment variable not set.")
        sys.exit(1)

    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    intents.guilds = True

    bot = HyperscoutBot(intents=intents)

    try:
        logging.info("Starting Hyperscout...")
        await bot.start(bot_token)
    except discord.errors.LoginFailure:
        logging.error("Failed to log in. Please check the HYPERSCOUT_BOT_TOKEN.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        if not bot.is_closed():
            await bot.close()
        logging.info("Hyperscout has been shut down.")

def main():
    # If there are command-line arguments, assume it's a CLI command.
    if len(sys.argv) > 1:
        cli()
    else:
        try:
            asyncio.run(start_bot())
        except KeyboardInterrupt:
            logging.info("Shutting down Hyperscout.")

if __name__ == "__main__":
    main()
