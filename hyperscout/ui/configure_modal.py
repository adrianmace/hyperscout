import discord
from hyperscout.database import configure_guild
from hyperscout.tracing import get_tracer

tracer = get_tracer(__name__)

class ConfigureModal(discord.ui.Modal, title='Configure Hyperscout'):
    destination_channel = discord.ui.Label(
        text='Destination Channel',
        description='Select the channel where notifications should be sent.',
        component=discord.ui.ChannelSelect(
            placeholder='Choose a channel...',
            channel_types=[discord.ChannelType.text],
        ),
    )

    spam_protection = discord.ui.Label(
        text='Spam Protection',
        description='Avoid sending the same notification within x minutes.',
        component=discord.ui.Select(
            placeholder='Choose a spam protection level...',
            options=[
                discord.SelectOption(label='0 minutes (disabled)', value='0'),
                discord.SelectOption(label='5 minutes', value='5', default=True),
                discord.SelectOption(label='10 minutes', value='10'),
                discord.SelectOption(label='15 minutes', value='15'),
            ],
        ),
    )

    delete_after = discord.ui.Label(
        text='Delete After...',
        description='Delete the notifications after x days.',
        component=discord.ui.Select(
            placeholder='Choose a deletion period...',
            options=[
                discord.SelectOption(label='1 day', value='1440', default=True),
                discord.SelectOption(label='2 days', value='2880'),
                discord.SelectOption(label='3 days', value='4320'),
                discord.SelectOption(label='Never (disabled)', value='0'),
            ],
        ),
    )

    async def on_submit(self, interaction: discord.Interaction):
        assert isinstance(self.destination_channel.component, discord.ui.ChannelSelect)
        assert isinstance(self.spam_protection.component, discord.ui.Select)
        assert isinstance(self.delete_after.component, discord.ui.Select)

        destination_channel_id = int(self.destination_channel.component.values[0].id)
        spam_protection_minutes = int(self.spam_protection.component.values[0])
        delete_after_minutes = int(self.delete_after.component.values[0])

        await configure_guild(
            interaction.guild.id,
            destination_channel_id,
            spam_protection_minutes,
            delete_after_minutes
        )

        with tracer.start_as_current_span("guild_configured") as span:
            span.set_attribute("guild.id", interaction.guild.id)
            span.set_attribute("guild.name", interaction.guild.name)
            span.set_attribute("destination_channel.id", destination_channel_id)
            span.set_attribute("spam_protection.minutes", spam_protection_minutes)
            span.set_attribute("delete_after.minutes", delete_after_minutes)

        await interaction.response.send_message(f"Successfully configured the bot.", ephemeral=True)
