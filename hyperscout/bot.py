import discord
import random
import re
import logging
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .database import get_all_guilds, get_guild_by_id, configure_guild
from discord.ext import commands
from discord.ui import View, ChannelSelect

logger = logging.getLogger('discord')

class HyperscoutBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.scheduler = AsyncIOScheduler(timezone=timezone.utc)
        self.scheduler.add_job(self.purge_bot_messages, 'cron', hour=0, minute=0)

    def is_member_joined(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Determines if a member has joined a voice channel, ignoring moves to and from the AFK channel."""
        afk_channel = member.guild.afk_channel
        afk_channel_id = afk_channel.id if afk_channel else None

        was_in_joinable_state = before.channel is None or before.channel.id == afk_channel_id
        is_in_valid_channel = after.channel is not None and after.channel.id != afk_channel_id

        return was_in_joinable_state and is_in_valid_channel

    async def send_join_message(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild_config = get_guild_by_id(member.guild.id)
        if not guild_config:
            return

        _, destination_channel_id = guild_config
        destination = await self.fetch_channel(int(destination_channel_id))

        messages = [
            "stumbled into", "crash-landed in", "respawned at", "accidentally joined",
            "teleported awkwardly into", "is vibing in", "materialized suspiciously in",
            "snuck into", "rolled into", "phased into existence in", "just glitched into",
            "tripped and fell into", "is kicking back in", "yeeted themselves into",
            "opened a portal and walked into"
        ]
        message_text = random.choice(messages)
        final_message = f'{member.display_name} {message_text} {after.channel.name}!'

        five_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=5)
        pattern = re.compile(f"^{re.escape(member.display_name)}.*{re.escape(after.channel.name)}!$")

        async for message in destination.history(limit=100, after=five_minutes_ago):
            if message.author == self.user and pattern.match(message.content):
                logger.info(f"Skipping message for {member.display_name} in {member.guild.name}'s {after.channel.name} channel because a similar one was sent recently.")
                return

        logger.info(f"Sending message '{final_message}' to {member.guild.name}'s #{destination.name}")
        await destination.send(final_message, allowed_mentions=discord.AllowedMentions.none())

    async def purge_bot_messages(self):
        guilds = get_all_guilds()
        for _, destination_channel_id in guilds:
            channel = await self.fetch_channel(int(destination_channel_id))
            async for message in channel.history():
                if message.author == self.user:
                    await message.delete()


    # Events
    # --------------------------------
    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        logger.info(f'We have logged in as {self.user}')
        self.scheduler.start()

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if self.is_member_joined(member, before, after):
            await self.send_join_message(member, before, after)
    
class ConfigureMenu(View):
    @discord.ui.select(
        cls=ChannelSelect, 
        channel_types=[discord.ChannelType.text], 
        placeholder="Select a channel..."
    )
    async def select_channels(self, interaction: discord.Interaction, select: ChannelSelect):
        destination_channel = select.values[0]
        configure_guild(interaction.guild.id, destination_channel.id)
        await interaction.response.send_message(f"Successfully configured #{destination_channel.name} as the destination channel.", ephemeral=True)
