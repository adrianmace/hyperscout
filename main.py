import discord
import os
import random
import logging

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def is_member_joined(before, after):
    if before.channel == None and after.channel != None:
        return True
    return False

@client.event
async def on_ready():
    logger = logging.getLogger('discord')
    logger.info(f'We have logged in as {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
    logger = logging.getLogger('discord')
    if is_member_joined(before, after):
        destination = await client.fetch_channel(os.getenv('HYPERSCOUT_DESTINATION_CHANNEL_ID'))

        messages = [
            "is now hanging out in",
            "has joined",
            "is chilling in",
            "jumped into",
            "entered",
            "is vibing in",
            "is now in"
        ]
        message_text = random.choice(messages)

        final_message = f'{member.display_name} {message_text} {after.channel.name}!'
        logger.info(final_message)

        await destination.send(final_message, delete_after=3600)

if __name__ == "__main__":
    client.run(os.getenv('HYPERSCOUT_BOT_TOKEN'))
