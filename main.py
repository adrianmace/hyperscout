import discord
import os
import random
import re
import logging
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger('discord')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def is_member_joined(before: discord.VoiceState, after: discord.VoiceState, afk_channel: int):
    if (before.channel is None or before.channel.id == afk_channel) and not (after.channel is None or after.channel.id == afk_channel):
            return True
    return False

def is_afk(guild: discord.Guild, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel.name == "Away" and not after.channel is None:
        return True
    return False

async def send_join_message(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    destination = await client.fetch_channel(os.getenv('HYPERSCOUT_DESTINATION_CHANNEL_ID'))

    messages = [
        "stumbled into",
        "crash-landed in",
        "respawned at",
        "accidentally joined",
        "teleported awkwardly into",
        "is vibing in",
        "materialized suspiciously in",
        "snuck into",
        "rolled into",
        "phased into existence in",
        "just glitched into",
        "tripped and fell into",
        "is kicking back in",
        "yeeted themselves into",
        "opened a portal and walked into"
    ]

    message_text = random.choice(messages)

    final_message = f'{member.display_name} {message_text} {after.channel.name}!'

    five_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=5)

    pattern = re.compile(f"^{re.escape(member.display_name)}.*{re.escape(after.channel.name)}!$")

    async for message in destination.history(limit=100, after=five_minutes_ago):
        if message.author == client.user and pattern.match(message.content):
            logger.info(f"Skipping message for {member.display_name} in {after.channel.name} because a similar one was sent recently.")
            return

    logger.info(f"Sending message: '{final_message}'")

    await destination.send( final_message, allowed_mentions=discord.AllowedMentions.none())

async def purge_bot_messages():
    channel = await client.fetch_channel(os.getenv('HYPERSCOUT_DESTINATION_CHANNEL_ID'))
    async for message in channel.history():
        if message.author == client.user:
            await message.delete()

scheduler = AsyncIOScheduler(timezone=timezone.utc)
scheduler.add_job(purge_bot_messages, 'cron', hour=12, minute=0)

@client.event
async def on_ready():
    logger.info(f'We have logged in as {client.user}')
    scheduler.start()

@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    afk_channel = member.guild.afk_channel.id
    if is_member_joined(before, after, afk_channel):
        await send_join_message(member, before, after)

if __name__ == "__main__":
    client.run(os.getenv('HYPERSCOUT_BOT_TOKEN'))
