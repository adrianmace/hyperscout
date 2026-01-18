from datetime import timezone, timedelta, datetime
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from hyperscout.database import get_all_guilds

class PurgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone=timezone.utc)
        self.scheduler.add_job(self.purge_bot_messages, 'cron', hour=0, minute=0)
        self.scheduler.start()

    async def purge_bot_messages(self):
        guilds = await get_all_guilds()
        for _, destination_channel_id, _, delete_after_minutes in guilds:
            if delete_after_minutes == 0:
                continue

            channel = await self.bot.fetch_channel(int(destination_channel_id))

            # Calculate the cutoff date for message deletion
            cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=delete_after_minutes)

            await channel.purge(before=cutoff_date, check=lambda m: m.author == self.bot.user)

async def setup(bot):
    await bot.add_cog(PurgeCog(bot))
