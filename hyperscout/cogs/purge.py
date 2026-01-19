import logging
from datetime import timezone, timedelta, datetime
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from hyperscout.database import get_all_guilds

logger = logging.getLogger(__name__)

class PurgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone=timezone.utc)
        self.scheduler.add_job(self.purge_bot_messages, 'cron', hour='*', minute=0)
        self.scheduler.start()

    async def purge_bot_messages(self):
        logger.info("Starting hourly message purge.", extra={"event": "purge_start"})
        guilds = await get_all_guilds()
        for guild_id, destination_channel_id, _, delete_after_minutes in guilds:
            if delete_after_minutes == 0:
                logger.warning(
                    f"Skipping purge for guild {guild_id} because delete_after_minutes is 0.",
                    extra={"event": "purge_skip", "guild_id": guild_id}
                )
                continue

            try:
                channel = await self.bot.fetch_channel(int(destination_channel_id))
                cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=delete_after_minutes)
                logger.info(
                    f"Purging messages before {cutoff_date} from channel {destination_channel_id} in guild {guild_id}.",
                    extra={
                        "event": "purge_processing",
                        "guild_id": guild_id,
                        "channel_id": destination_channel_id,
                        "cutoff_date": cutoff_date
                    }
                )
                purged_messages = await channel.purge(before=cutoff_date, check=lambda m: m.author == self.bot.user)
                logger.info(
                    f"Purged {len(purged_messages)} messages from channel {destination_channel_id} in guild {guild_id}.",
                    extra={
                        "event": "purge_success",
                        "guild_id": guild_id,
                        "channel_id": destination_channel_id,
                        "purged_count": len(purged_messages)
                    }
                )
            except Exception as e:
                logger.error(
                    f"Failed to purge messages for guild {guild_id}.",
                    extra={"event": "purge_error", "guild_id": guild_id, "error": str(e)}
                )
        logger.info("Finished hourly message purge.", extra={"event": "purge_finish"})

async def setup(bot):
    await bot.add_cog(PurgeCog(bot))
