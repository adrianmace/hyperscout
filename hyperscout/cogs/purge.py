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
        with tracer.start_as_current_span("hourly_purge_job") as parent_span:
            guilds = await get_all_guilds()
            parent_span.set_attribute("guild_count", len(guilds))

            for guild_id, destination_channel_id, _, delete_after_minutes in guilds:
                with tracer.start_as_current_span("purge_guild_messages") as child_span:
                    child_span.set_attribute("guild.id", guild_id)

                    if delete_after_minutes == 0:
                        child_span.set_attribute("result", "skipped")
                        child_span.set_attribute("reason", "delete_after_minutes is 0")
                        continue

                    try:
                        child_span.set_attribute("destination_channel.id", destination_channel_id)
                        channel = await self.bot.fetch_channel(int(destination_channel_id))
                        cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=delete_after_minutes)
                        child_span.set_attribute("cutoff_date", str(cutoff_date))

                        purged_messages = await channel.purge(before=cutoff_date, check=lambda m: m.author == self.bot.user)

                        child_span.set_attribute("result", "success")
                        child_span.set_attribute("purged_count", len(purged_messages))
                    except Exception as e:
                        child_span.set_attribute("result", "error")
                        child_span.record_exception(e)

async def setup(bot):
    await bot.add_cog(PurgeCog(bot))
