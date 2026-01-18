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
        logging.info(f"{interaction.user.name} triggered /configure in {interaction.guild.name}")
        await interaction.response.send_modal(ConfigureModal())

async def setup(bot):
    await bot.add_cog(ConfigureCog(bot))
