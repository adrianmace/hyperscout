import discord
import logging
from discord.ext import commands

logger = logging.getLogger('discord')

class HyperscoutBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    # Events
    # --------------------------------
    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        logger.info(f'We have logged in as {self.user}')
        await self.change_presence(activity=discord.Game("/configure"))

    async def on_guild_join(self, guild: discord.Guild):
        logger.info(f"We've been added to {guild.name}!")
