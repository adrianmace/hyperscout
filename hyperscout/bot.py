import discord
from discord.ext import commands
from hyperscout.tracing import get_tracer

tracer = get_tracer(__name__)

class HyperscoutBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    # Events
    # --------------------------------
    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        with tracer.start_as_current_span("logged_in") as span:
            span.set_attribute("user", str(self.user))
        await self.change_presence(activity=discord.Game("/configure"))

    async def on_guild_join(self, guild: discord.Guild):
        with tracer.start_as_current_span("guild_join") as span:
            span.set_attribute("guild.id", guild.id)
            span.set_attribute("guild.name", guild.name)
