import discord
import random
import re
import logging
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger('discord')

class HyperscoutBot(discord.Client):
    def __init__(self, bot_token, destination_channel_id, intents):
        super().__init__(intents=intents)
        self.bot_token = bot_token
        self.destination_channel_id = destination_channel_id
        self.scheduler = AsyncIOScheduler(timezone=timezone.utc)
        self.scheduler.add_job(self.purge_bot_messages, 'cron', hour=0, minute=0)

    def is_member_joined(self, before: discord.VoiceState, after: discord.VoiceState):
        afk_channel_id = before.channel.guild.afk_channel.id if before.channel and before.channel.guild.afk_channel else None
        if (before.channel is None or before.channel.id == afk_channel_id) and \
           not (after.channel is None or after.channel.id == afk_channel_id):
            return True
        return False

    async def send_join_message(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        destination = await self.fetch_channel(self.destination_channel_id)

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
                logger.info(f"Skipping message for {member.display_name} in {after.channel.name} because a similar one was sent recently.")
                return

        logger.info(f"Sending message: '{final_message}'")
        await destination.send(final_message, allowed_mentions=discord.AllowedMentions.none())

    async def purge_bot_messages(self):
        channel = await self.fetch_channel(self.destination_channel_id)
        async for message in channel.history():
            if message.author == self.user:
                await message.delete()

    async def on_ready(self):
        logger.info(f'We have logged in as {self.user}')
        self.scheduler.start()

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if self.is_member_joined(before, after):
            await self.send_join_message(member, before, after)
