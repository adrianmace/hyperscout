import os
import sys
import asyncio
import discord

from hyperscout.database import initialize_database, migrate_schema
from hyperscout.bot import HyperscoutBot
from hyperscout.cli import cli
from hyperscout.tracing import setup_tracing, get_tracer

# Configure tracing
setup_tracing()
tracer = get_tracer(__name__)

async def start_bot():
    """
    Initializes the database and runs the single bot client.
    """
    await initialize_database()
    await migrate_schema()

    bot_token = os.getenv('HYPERSCOUT_BOT_TOKEN')
    if not bot_token:
        with tracer.start_as_current_span("startup_error") as span:
            span.set_attribute("error_code", "missing_token")
            span.record_exception(Exception("HYPERSCOUT_BOT_TOKEN environment variable not set."))
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
        with tracer.start_as_current_span("startup"):
            await bot.start(bot_token)
    except discord.errors.LoginFailure as e:
        with tracer.start_as_current_span("login_failure") as span:
            span.record_exception(e)
    except Exception as e:
        with tracer.start_as_current_span("unexpected_error") as span:
            span.record_exception(e)
    finally:
        if not bot.is_closed():
            await bot.close()
        with tracer.start_as_current_span("shutdown"):
            pass

def main():
    # If there are command-line arguments, assume it's a CLI command.
    if len(sys.argv) > 1:
        cli()
    else:
        try:
            asyncio.run(start_bot())
        except KeyboardInterrupt:
            with tracer.start_as_current_span("shutdown_request"):
                pass

if __name__ == "__main__":
    main()
