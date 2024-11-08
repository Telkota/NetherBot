from discord.ext import commands
import discord


def setup(bot):
    @bot.command(name="moveall", help="Move all members current connected to a voice channel into your specified channel")
    @commands.has_guild_permissions(move_members=True)
    async def move_all(ctx, target_channel_name: str = None):
        #if no target parameter is entered, return an error message and quit.
        if target_channel_name is None:
            await ctx.send("Error: No target channel name provided. Please specify a target channel.")
            return
        
        try:
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

        except Exception as e:
            await ctx.send("An error occurred while trying to move users.")
            print(f"Error in move_all: {e}")

    @bot.command(name="move", help="Move a member to a different voice channel")
    @commands.has_guild_permissions(move_members=True)
    async def move(ctx, member: discord.Member = None, target_channel_name: str = None):
        #if no target or member parameter is entered, return an error message and quit.
        if member is None and target_channel_name is None:
            await ctx.send(f"Error: You didn't specify a user nor target channel.\n"
                           "To use this command, provide a user and target channel.\n"
                           "`!move <user> <target-channel>`")
            return
        elif target_channel_name is None:
            await ctx.send("Error: You didn't specify a target channel.")
            return
        
        try:
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

        except Exception as e:
            await ctx.send("An error occured while trying to move the user")
            print(f"Error in move: {e}")
    
    @bot.command(name="kick", help="Kick a member")
    @commands.has_guild_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member = None, *, reason=None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await ctx.send("Error: You didn't input a user to kick.")
            return
        
        try:
            await member.kick(reason=reason)
            #if reason is given - Display reason
            if reason is not None:
                await ctx.send(f"Kicked {member}. Reason: {reason}")
            #Otherwise - Display just kick message
            else:
                await ctx.send(f"Kicked {member}")

        except Exception as e:
            await ctx.send("An error occured while trying to kick the user.")
            print(f"Error in kick: {e}")

    @bot.command(name="ban", help="Ban a member")
    @commands.has_guild_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member = None, *, reason=None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await ctx.send("Error: You didn't input a user to ban.")
            return
        
        try:
            await member.ban(reason=reason)
            #if reason is given - Display reason
            if reason is not None:
                await ctx.send(f"Banned {member}. Reason: {reason}")
            #Otherwise - Display just ban message
            else:
                await ctx.send(f"Banned {member}")

        except Exception as e:
            await ctx.send("An error occured while trying to ban the user.")
            print(f"Error in ban: {e}")

    @bot.command(name="mute", help="Mute a member in voice")
    @commands.has_guild_permissions(mute_members=True)
    async def mute(ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await ctx.send("Error: You didn't input a user to mute.")
            return
        
        try:
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

        except Exception as e:
            await ctx.send("An error occured while trying to mute the user.")
            print(f"Error in mute: {e}")
    
    @bot.command(name="deafen", help="Deafen a member in voice")
    @commands.has_guild_permissions(deafen_members=True)
    async def deafen(ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await ctx.send("Error: You didn't input a user to deafen.")
            return
        
        try:
            #check if the user is in a voice channel
            if member.voice is None:
                await ctx.send(f"{member} is not in a voice channel. Muting is unnecessary.")
                return
            #check if the user is already deafened
            if member.voice.deaf:
                await ctx.send(f"{member} is already deafened.")
                return
            
            await member.edit(deaf=True)
            await ctx.send(f"Deafened {member}")

        except Exception as e:
            await ctx.send("An error occured while trying to deafen the user.")
            print(f"Error in deafen: {e}")
    
    @bot.command(name="unmute", help="Unmute a member in voice")
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await ctx.send("Error: You didn't input a user to unmute.")
            return
        
        try:
            #check if the user is already unmuted
            if not member.voice.mute:
                await ctx.send(f"{member} is already unmuted.")
                return

            await member.edit(mute=False)
            await ctx.send(f"Unmuted {member}")

        except Exception as e:
            await ctx.send("An error occured while trying to unmute the user.")
            print(f"Error in unmute: {e}")
    
    @bot.command(name="undeafen", help="Undeafen a member in voice")
    @commands.has_guild_permissions(deafen_members=True)
    async def undeafen(ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await ctx.send("Error: You didn't input a user to undeafen.")
            return
        
        try:
            #check if the user is already undeafened
            if not member.voice.deaf:
                await ctx.send(f"{member} is already undeafened.")
                return
            
            await member.edit(deaf=False)
            await ctx.send(f"Undeafened {member}")

        except Exception as e:
            await ctx.send("An error occured while trying to undeafen the user.")
            print(f"Error in undeafen: {e}")
    
    @bot.command(name="silence", help="Mutes and Deafens a member in voice.")
    @commands.has_guild_permissions(deafen_members=True)
    @commands.has_guild_permissions(mute_members=True)
    async def silence(ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await ctx.send("Error: You didn't input a user to silence.")
            return

        try:
            #check if the user is already silenced
            if member.voice.deaf and member.voice.mute:
                await ctx.send(f"{member} is already silenced.")
                return
            
            #check if the user is already muted but not deafened
            if member.voice.mute and not member.voice.deaf:
                await member.edit(deaf=True)
                await ctx.send(f"{member} was already muted but not deafened - I've deafened them.")
                return
            
            #check if the user is already deafened but not muted
            if member.voice.deaf and not member.voice.mute:
                await member.edit(mute=True)
                await ctx.send(f"{member} was already deafened but not muted - I've muted them.")
                return
            
            await member.edit(mute=True, deaf=True)
            await ctx.send(f"{member} has been silenced.")
        
        except Exception as e:
            await ctx.send("An error occured while trying to silence the user.")
            print(f"Error in silence: {e}")
    
    @bot.command(name="unsilence", help="Unmutes and Undeafens a member in voice")
    @commands.has_guild_permissions(deafen_members=True)
    @commands.has_guild_permissions(mute_members=True)
    async def unsilence(ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await ctx.send("Error: You didn't input a user to unsilence.")
            return
        
        try:
            #check if the user is already unsilenced
            if not member.voice.deaf and not member.voice.mute:
                await ctx.send(f"{member} isn't muted or deafened.")
                return
            
            #Check if the user is muted but not deafened
            if member.voice.mute and not member.voice.deaf:
                await member.edit(mute=False)
                await ctx.send(f"{member} was unmuted. {member} wasn't deafened to begin with.")
                return

            #Check if the user is deafened but not muted
            if member.voice.deaf and not member.voice.mute:
                await member.edit(deaf=False)
                await ctx.send(f"{member} was undeafened. {member} wasn't muted to begin with.")
                return

            await member.edit(mute=False, deaf=False)
            await ctx.send(f"{member} was unsilenced. They can speak and hear again!")

        except Exception as e:
            await ctx.send("An error occured while trying to unsilence the user.")
            print(f"Error in unsilence: {e}")