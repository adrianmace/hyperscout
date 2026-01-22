from datetime import timezone, timedelta, datetime
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from hyperscout.database import get_all_guilds
from hyperscout.tracing import get_tracer

tracer = get_tracer(__name__)

class PurgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone=timezone.utc)
        self.scheduler.add_job(self.purge_bot_messages, 'cron', hour='*', minute=0)
        self.scheduler.start()

    async def purge_bot_messages(self):
        with tracer.start_as_current_span("purge_start"):
            guilds = await get_all_guilds()
            for guild_id, destination_channel_id, _, delete_after_minutes in guilds:
                if delete_after_minutes == 0:
                    with tracer.start_as_current_span("purge_skip") as span:
                        span.set_attribute("guild_id", guild_id)
                    continue

                try:
                    channel = await self.bot.fetch_channel(int(destination_channel_id))
                    cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=delete_after_minutes)
                    with tracer.start_as_current_span("purge_processing") as span:
                        span.set_attribute("guild_id", guild_id)
                        span.set_attribute("channel_id", destination_channel_id)
                        span.set_attribute("cutoff_date", str(cutoff_date))
                    purged_messages = await channel.purge(before=cutoff_date, check=lambda m: m.author == self.bot.user)
                    with tracer.start_as_current_span("purge_success") as span:
                        span.set_attribute("guild_id", guild_id)
                        span.set_attribute("channel_id", destination_channel_id)
                        span.set_attribute("purged_count", len(purged_messages))
                except Exception as e:
                    with tracer.start_as_current_span("purge_error") as span:
                        span.set_attribute("guild_id", guild_id)
                        span.record_exception(e)
            with tracer.start_as_current_span("purge_finish"):
                pass

async def setup(bot):
    await bot.add_cog(PurgeCog(bot))
