from discord.ext import commands
import discord

def setup(bot):
    @bot.command(name="moveall", help="Move all members current connected to a voice channel into your specified channel")
    @commands.has_permissions(move_members=True)
    async def move_all(ctx, target_channel_name: str):
        target_channel = None
        target_name_lower = target_channel_name.lower()

        #Find the target channel by partial name match. Case insensitive
        for vc in ctx.guild.voice_channels:
            if target_name_lower in vc.name.lower():
                target_channel = vc
                break
        
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
    async def move(ctx, member: discord.Member, target_channel_name: str):
        target_channel = None
        target_name_lower = target_channel_name.lower()

        #Find the target channel by partial name match. Case insensitive
        for vc in ctx.guild.voice_channels:
            if target_name_lower in vc.name.lower():
                target_channel = vc
                break
        
        #check to see if the target channel exists
        if target_channel:
            await member.move_to(target_channel)
            await ctx.send(f"Moved {member} to {target_channel.name}")
        #if the target channel is invalid
        else:
            await ctx.send("Invalid target channel name provided.")
    
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

    @bot.command(name="mute", help="Mute a member in voice")
    @commands.has_permissions(mute_members=True)
    async def mute(ctx, member: discord.Member):
        #check if the user is in a voice channel
        if member.voice is None:
            await ctx.send(f"{member} is not in a voice channel. Muting is unnecessary.")
            return
        #check if the user is already muted
        if member.voice.mute:
            await ctx.send(f"{member} is already muted.")
            return
        
        await member.edit(mute=True)
        await ctx.send(f"Muted {member}")
    
    @bot.command(name="deafen", help="Deafen a member in voice")
    @commands.has_permissions(deafen_members=True)
    async def deafen(ctx, member: discord.Member):
        #check if the user is in a voice channel
        if member.voice is None:
            await ctx.send(f"{member} is not in a voice channel. Muting is unnecessary.")
            return
        #check if the user is already deafened
        if member.voice.deaf:
            await ctx.send(f"{member} is already deafened.")
            return
        
        await member.edit(deafen=True)
        await ctx.send(f"Deafened {member}")
    
    @bot.command(name="unmute", help="Unmute a member in voice")
    @commands.has_permissions(mute_members=True)
    async def unmute(ctx, member: discord.Member):
        #check if the user is already unmuted
        if not member.voice.mute:
            await ctx.send(f"{member} is already unmuted.")
            return

        await member.edit(mute=False)
        await ctx.send(f"Unmuted {member}")
    
    @bot.command(name="undeafen", help="Undeafen a member in voice")
    @commands.has_permissions(deafen_members=True)
    async def undeafen(ctx, member: discord.Member):
        #check if the user is already undeafened
        if not member.voice.deaf:
            await ctx.send(f"{member} is already undeafened.")
            return
        
        await member.edit(deafen=False)
        await ctx.send(f"Undeafened {member}")