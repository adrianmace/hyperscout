import discord
import logging
from discord.ui import View, ChannelSelect, Select, Button
from hyperscout.database import configure_guild

class ConfigureView(View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot

        # State
        self.destination_channel_id = None
        self.spam_protection_minutes = 5 # Default
        self.delete_after_days = 1 # Default

        # --- Components ---

        # Destination Channel Select
        self.channel_select = ChannelSelect(
            placeholder="Select a destination channel...",
            channel_types=[discord.ChannelType.text],
            row=0
        )
        self.channel_select.callback = self.channel_select_callback
        self.add_item(self.channel_select)

        # Spam Protection Select
        spam_options = [
            discord.SelectOption(label="0 minutes (disabled)", value="0"),
            discord.SelectOption(label="5 minutes", value="5", default=True),
            discord.SelectOption(label="10 minutes", value="10"),
            discord.SelectOption(label="15 minutes", value="15"),
        ]
        self.spam_select = Select(
            placeholder="Spam Protection: Avoid sending the same notification within x minutes.",
            options=spam_options,
            row=1
        )
        self.spam_select.callback = self.spam_select_callback
        self.add_item(self.spam_select)

        # Delete After Select
        delete_options = [
            discord.SelectOption(label="1 day", value="1", default=True),
            discord.SelectOption(label="2 days", value="2"),
            discord.SelectOption(label="3 days", value="3"),
            discord.SelectOption(label="Never (disabled)", value="0"),
        ]
        self.delete_select = Select(
            placeholder="Delete After...: Delete the notifications after x days.",
            options=delete_options,
            row=2
        )
        self.delete_select.callback = self.delete_select_callback
        self.add_item(self.delete_select)

        # Save Button
        self.save_button = Button(label="Save", style=discord.ButtonStyle.primary, row=3)
        self.save_button.callback = self.save_button_callback
        self.add_item(self.save_button)

    async def channel_select_callback(self, interaction: discord.Interaction):
        self.destination_channel_id = int(self.channel_select.values[0].id)
        await interaction.response.defer()

    async def spam_select_callback(self, interaction: discord.Interaction):
        self.spam_protection_minutes = int(self.spam_select.values[0])
        await interaction.response.defer()

    async def delete_select_callback(self, interaction: discord.Interaction):
        self.delete_after_days = int(self.delete_select.values[0])
        await interaction.response.defer()

    async def save_button_callback(self, interaction: discord.Interaction):
        if not self.destination_channel_id:
            await interaction.response.send_message("Please select a destination channel first.", ephemeral=True)
            return

        await configure_guild(
            interaction.guild.id,
            self.destination_channel_id,
            self.spam_protection_minutes,
            self.delete_after_days
        )
        logging.info(f"{interaction.guild.name} is now configured.")
        await interaction.response.send_message(f"Successfully configured the bot.", ephemeral=True)
