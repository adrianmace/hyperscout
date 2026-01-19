import discord
import random
import re
import logging
from datetime import datetime, timedelta, timezone
from discord.ext import commands
from hyperscout.database import get_guild_by_id

logger = logging.getLogger(__name__)

class VoiceEventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_member_joined(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Determines if a member has joined a voice channel, ignoring moves to and from the AFK channel."""
        afk_channel = member.guild.afk_channel
        afk_channel_id = afk_channel.id if afk_channel else None

        was_in_joinable_state = before.channel is None or before.channel.id == afk_channel_id
        is_in_valid_channel = after.channel is not None and after.channel.id != afk_channel_id

        return was_in_joinable_state and is_in_valid_channel

    async def send_join_message(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild_config = await get_guild_by_id(member.guild.id)
        if not guild_config:
            return

        _, destination_channel_id, spam_protection_minutes, _ = guild_config
        destination = await self.bot.fetch_channel(int(destination_channel_id))

        # Spam protection - do not send if the spam protection value is not 0
        if spam_protection_minutes > 0:
            spam_protection_delta = datetime.now(timezone.utc) - timedelta(minutes=spam_protection_minutes)
            pattern = re.compile(f"^{re.escape(member.display_name)}.*{re.escape(after.channel.name)}!$")
            async for message in destination.history(after=spam_protection_delta):
                if message.author == self.bot.user and pattern.match(message.content):
                    logger.info(
                        "Skipping message due to spam protection.",
                        extra={
                            "event": "spam_protection_skip",
                            "guild_id": member.guild.id,
                            "member_id": member.id,
                            "channel_id": after.channel.id
                        }
                    )
                    return

        messages = [
            "stumbled into", "crash-landed in", "respawned at", "accidentally joined",
            "teleported awkwardly into", "is vibing in", "materialized suspiciously in",
            "snuck into", "rolled into", "phased into existence in", "just glitched into",
            "tripped and fell into", "is kicking back in", "yeeted themselves into",
            "opened a portal and walked into"
        ]
        message_text = random.choice(messages)
        final_message = f'{member.display_name} {message_text} {after.channel.name}!'

        logger.info(
            "Sending voice channel join message.",
            extra={
                "event": "send_join_message",
                "guild_id": member.guild.id,
                "member_id": member.id,
                "channel_id": after.channel.id,
                "final_message": final_message
            }
        )
        await destination.send(final_message, allowed_mentions=discord.AllowedMentions.none())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if self.is_member_joined(member, before, after):
            await self.send_join_message(member, before, after)

async def setup(bot):
    await bot.add_cog(VoiceEventsCog(bot))
