import asyncio
import sys
import discord
import logging

from hyperscout.database import get_all_servers, initialize_database
from hyperscout.bot import HyperscoutBot
from hyperscout.cli import cli

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def start_bot(server_name, bot_token, destination_channel_id, intents):
    """Creates, starts, and handles a single bot instance."""
    bot = HyperscoutBot(
        bot_token=bot_token,
        destination_channel_id=int(destination_channel_id),
        intents=intents
    )
    try:
        logging.info(f"Starting bot for server: {server_name}")
        await bot.start(bot_token)
    except discord.errors.LoginFailure:
        logging.error(f"Failed to log in for bot on server '{server_name}'. Please check the token.")
    except Exception as e:
        logging.error(f"An unexpected error occurred for bot on server '{server_name}': {e}")
    finally:
        if not bot.is_closed():
            await bot.close()
        logging.info(f"Bot for server '{server_name}' has been closed.")


async def main():
    """
    Initializes the database, fetches server configurations,
    and runs a bot for each server concurrently.
    """
    initialize_database()
    servers = get_all_servers()

    if not servers:
        logging.warning("No server configurations found in the database. Run the 'set' command to add a server.")
        return

    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    tasks = [
        start_bot(server_name, bot_token, destination_channel_id, intents)
        for server_name, bot_token, destination_channel_id in servers
    ]

    if tasks:
        await asyncio.gather(*tasks)
    else:
        logging.info("No bots to start.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli()
    else:
        logging.info("Starting Hyperscout in bot mode...")
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logging.info("Shutting down Hyperscout.")
