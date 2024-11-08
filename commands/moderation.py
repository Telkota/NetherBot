from discord.ext import commands
import discord

def setup(bot):
    @bot.command(name="moveall", help="Move all members current connected to a voice channel into your specified channel")
    @commands.has_permissions(move_members=True)
    async def move_all(ctx, target_channel_name: str):
        target_channel = discord.utils.get(ctx.guild.voice_channels, name=target_channel_name)
        
        #check to see if the target channel exists
        if target_channel:
            for voice_channel in ctx.guild.voice_channels:          #loop over each voice channel
                if voice_channel != target_channel:                 #as long as the channel is not the target
                    for member in voice_channel.members:            #move each member in that channel into the target
                        await member.move_to(target_channel)
            #confirmation message that it was successful
            await ctx.send(f"All members moved to {target_channel.name} from other voice channels")
        #if the target channel is invalid
        else:
            await ctx.send("Invalid target channel name provided.")

    @bot.command(name="move", help="Move a member to a different voice channel")
    @commands.has_guild_permissions(move_members=True)
    async def move(ctx, member: discord.Member, channel: discord.VoiceChannel):
        await member.move_to(channel)
        await ctx.send(f"Moved {member} to {channel.name}")
    
    @bot.command(name="kick", help="Kick a member")
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        #if reason is given - Display reason
        if reason is not None:
            await ctx.send(f"Kicked {member}. Reason: {reason}")
        #Otherwise - Display just kick message
        else:
            await ctx.send(f"Kicked {member}")

    @bot.command(name="ban", help="Ban a member")
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        #if reason is given - Display reason
        if reason is not None:
            await ctx.send(f"Banned {member}. Reason: {reason}")
        #Otherwise - Display just ban message
        else:
            await ctx.send(f"Banned {member}")