import discord
import os
import random
import logging

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def is_member_joined(before: discord.VoiceState, after: discord.VoiceState):
    if before.channel is None and not after.channel is None:
        return True
    return False

@client.event
async def on_ready():
    logger = logging.getLogger('discord')
    logger.info(f'We have logged in as {client.user}')

@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    logger = logging.getLogger('discord')
    if is_member_joined(before, after):
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

        final_message = f'{member.mention} {message_text} {after.channel.mention}!'
        logger.info(final_message)

        await destination.send(final_message, allowed_mentions=discord.AllowedMentions.none())

if __name__ == "__main__":
    client.run(os.getenv('HYPERSCOUT_BOT_TOKEN'))
