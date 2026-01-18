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
        for _, destination_channel_id, _, delete_after_days in guilds:
            if delete_after_days == 0:
                continue

            channel = await self.bot.fetch_channel(int(destination_channel_id))

            # Calculate the cutoff date for message deletion
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=delete_after_days)

            async for message in channel.history(before=cutoff_date):
                if message.author == self.bot.user:
                    await message.delete()

async def setup(bot):
    await bot.add_cog(PurgeCog(bot))
