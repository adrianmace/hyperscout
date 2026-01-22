import discord
from discord.ext import commands
from hyperscout.ui.configure_modal import ConfigureModal
from hyperscout.tracing import get_tracer

tracer = get_tracer(__name__)

class ConfigureCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='configure', description='Lets you configure Hyperscout\'s behaviours.')
    @discord.app_commands.default_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        with tracer.start_as_current_span("command_configure") as span:
            span.set_attribute("user_id", interaction.user.id)
            span.set_attribute("user_name", interaction.user.name)
            span.set_attribute("guild_id", interaction.guild.id)
            span.set_attribute("guild_name", interaction.guild.name)
        await interaction.response.send_modal(ConfigureModal())

async def setup(bot):
    await bot.add_cog(ConfigureCog(bot))
