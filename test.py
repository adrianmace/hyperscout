async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """An abstract method that is called when the client's voice state has changed. This corresponds to VOICE_STATE_UPDATE."""
        if not member.guild.id in TARGET_SERVERS:
            return
        if not before.channel is None and not after.channel is None:
            if before.channel.id == after.channel.id:
                return
        found_channel = False
        if not after.channel is None:
            if after.channel.id in TARGET_SERVERS[member.guild.id][1]:
                found_channel = True
        if not before.channel is None:
            if before.channel.id in TARGET_SERVERS[member.guild.id][1]:
                found_channel = True
        if found_channel:
            jlt = ""
            cname = ""
            if not before.channel is None:
                if before.channel.id in TARGET_SERVERS[before.channel.guild.id][1]:
                    jlt = "left"
                    cname = before.channel.mention
            if not after.channel is None:
                if after.channel.id in TARGET_SERVERS[after.channel.guild.id][1]:
                    jlt = "joined"
                    cname = after.channel.mention
            if not before.channel is None and not after.channel is None:
                if before.channel.id in TARGET_SERVERS[member.guild.id][1] and after.channel.id in TARGET_SERVERS[member.guild.id][1]:
                    await self.get_channel(TARGET_SERVERS[member.guild.id][0]).send(content=f"**{member.mention}** has switched from {before.channel.mention} to {after.channel.mention}!", allowed_mentions=discord.AllowedMentions.none())
                    return
            await self.get_channel(TARGET_SERVERS[member.guild.id][0]).send(content=f"**{member.mention}** has {jlt} {cname}!", allowed_mentions=discord.AllowedMentions.none())
