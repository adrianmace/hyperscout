import discord
import logging
from discord.ext import commands
from discord.ui import View, ChannelSelect
from hyperscout.database import configure_guild

class ConfigureMenu(View):
    @discord.ui.select(
        cls=ChannelSelect,
        channel_types=[discord.ChannelType.text],
        placeholder="Select a channel..."
    )
    async def select_channels(self, interaction: discord.Interaction, select: ChannelSelect):
        destination_channel = select.values[0]
        await configure_guild(interaction.guild.id, destination_channel.id)
        logging.info(f"{interaction.guild.name} is now configured to send alerts to #{destination_channel.name}")
        await interaction.response.send_message(f"Successfully configured #{destination_channel.name} as the destination channel.", ephemeral=True)

class ConfigureCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='configure', description='Lets you configure Hyperscout\'s behaviours.')
    @discord.app_commands.default_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        logging.info(f"{interaction.user.name} triggered /configure in {interaction.guild.name}")
        await interaction.response.send_message("Please select the channel where notifications should land...", view=ConfigureMenu(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(ConfigureCog(bot))
