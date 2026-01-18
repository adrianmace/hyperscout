import discord
import logging
from discord.ext import commands
from hyperscout.ui.configure_modal import ConfigureModal

class ConfigureCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='configure', description='Lets you configure Hyperscout\'s behaviours.')
    @discord.app_commands.default_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        logging.info(
            "Configure command triggered.",
            extra={
                "event": "command_configure",
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "guild_id": interaction.guild.id,
                "guild_name": interaction.guild.name
            }
        )
        await interaction.response.send_modal(ConfigureModal())

async def setup(bot):
    await bot.add_cog(ConfigureCog(bot))
