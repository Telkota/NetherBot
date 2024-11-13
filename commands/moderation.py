from discord.ext import commands
import utility.utils as u
import discord
import json
import logging

#enable logging
logging.basicConfig(level=logging.DEBUG)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #Move all function - command to move all users to a specific voice channel
    @commands.command(name="moveall", 
                      help="Move all users to one channel",
                      description="""Command to move all users current connected to a voice channel to one specific channel.
                      Handy for when there are users in different channels and you want to gather them all in one place.
                      
                      Required Permissions:
                      - move members""",
                      usage="[channel]",
                      aliases=["ma", "raidtime"])
    @commands.has_guild_permissions(move_members=True)
    async def move_all(self, ctx, target_channel_name: str = None):
        #if no target parameter is entered, return an error message and quit.
        if target_channel_name is None:
            await u.send_response(self.bot, ctx, "Error: No target channel name provided. Please specify a target channel.")
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
                await u.send_response(self.bot, ctx, f"All members moved to {target_channel.name} from other voice channels")

            #if the target channel is invalid
            else:
                await u.send_response(self.bot, ctx, "Invalid target channel name provided.")

        except Exception as e:
            await u.send_response(self.bot, ctx, "An error occurred while trying to move users.")
            print(f"Error in move_all: {e}")

    #Move function - Moves a user to a specific channel
    @commands.command(name="move", 
                      help="Move a member to a different voice channel",
                      description="""Move a user to a different voice channel.
                      Write in the user's name and target channel to move them!
                      
                      Required Permissions:
                      - Move Members""",
                      usage="[user] [target Channel]",
                      aliases=["mo"])
    @commands.has_guild_permissions(move_members=True)
    async def move(self, ctx, member: discord.Member = None, target_channel_name: str = None):
        #if no target or member parameter is entered, return an error message and quit.
        if member is None and target_channel_name is None:
            await u.send_response(self.bot, ctx, f"Error: You didn't specify a user nor target channel.\n"
                           "To use this command, provide a user and target channel.\n"
                           "`!move <user> <target-channel>`")
            return
        elif target_channel_name is None:
            await u.send_response(self.bot, ctx, "Error: You didn't specify a target channel.")
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
                await u.send_response(self.bot, ctx, f"Moved {member} to {target_channel.name}")

            #if the target channel is invalid
            else:
                await u.send_response(self.bot, ctx, "Invalid target channel name provided.")

        except Exception as e:
            await u.send_response(self.bot, ctx, "An error occured while trying to move the user")
            print(f"Error in move: {e}")
    
    #kick function - Kicks a user with or without a reason
    @commands.command(name="kick", 
                      help="Kick a member",
                      description="""Kick a user from your discord server.
                      Remove any obnoxious user from the server (temporarly).
                      The user could rejoin the server at any time.

                      Reason can be left empty.
                      
                      Required Permissions:
                      - Kick Members""",
                      usage="[user] [reason]",
                      aliases=["k", "ki"])
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason: str = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await u.send_response(self.bot, ctx, "Error: You didn't input a user to kick.")
            return
        
        try:
            await member.kick(reason=reason)
            #if reason is given - Display reason
            if reason is not None:
                await u.send_response(self.bot, ctx, f"Kicked {member}. Reason: {reason}")
            #Otherwise - Display just kick message
            else:
                await u.send_response(self.bot, ctx, f"Kicked {member}")

        except Exception as e:
            await u.send_response(self.bot, ctx, "An error occured while trying to kick the user.")
            print(f"Error in kick: {e}")

    #ban function - Bans a user with or without a reason
    @commands.command(name="ban", 
                      help="Ban a member",
                      description="""Ban a user from your server.
                      The user won't be able to rejoin your server until someone has gone in and manually unbanned them
                      
                      Reason can be left empty.

                      Required Permissions:
                      - Ban Members""",
                      usage="[user] [reason]",
                      aliases=["b", "bop"])
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason: str = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await u.send_response(self.bot, ctx, "Error: You didn't input a user to ban.")
            return
        
        try:
            await member.ban(reason=reason)
            #if reason is given - Display reason
            if reason is not None:
                await u.send_response(self.bot, ctx, f"Banned {member}. Reason: {reason}")
            #Otherwise - Display just ban message
            else:
                await u.send_response(self.bot, ctx, f"Banned {member}")

        except Exception as e:
            await u.send_response(self.bot, ctx, "An error occured while trying to ban the user.")
            print(f"Error in ban: {e}")

    #Mute function - Mutes a user if they are in a voice channel
    @commands.command(name="mute", 
                      help="Mute a member in voice",
                      description="""Mute a user in voice so they can't speak until unmuted

                      Required Permissions:
                      - Mute Members""",
                      usage="[user]")
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await u.send_response(self.bot, ctx, "Error: You didn't input a user to mute.")
            return
        
        try:
            #check if the user is in a voice channel
            if member.voice is None:
                await u.send_response(self.bot, ctx, f"{member} is not in a voice channel. Muting is unnecessary.")
                return
            #check if the user is already muted
            if member.voice.mute:
                await u.send_response(self.bot, ctx, f"{member} is already muted.")
                return
            
            await member.edit(mute=True)
            await u.send_response(self.bot, ctx, f"Muted {member}")

        except Exception as e:
            await u.send_response(self.bot, ctx, "An error occured while trying to mute the user.")
            print(f"Error in mute: {e}")
    
    #Deafen function - Deafens a user if they are in a voice channel.
    @commands.command(name="deafen", 
                      help="Deafen a member in voice",
                      description="""Deafens a user, leaving them unable to hear others until undeafened
                      
                      Required Permissions:
                      - Deafen Members""",
                      usage="[user]")
    @commands.has_guild_permissions(deafen_members=True)
    async def deafen(self, ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await u.send_response(self.bot, ctx, "Error: You didn't input a user to deafen.")
            return
        
        try:
            #check if the user is in a voice channel
            if member.voice is None:
                await u.send_response(self.bot, ctx, f"{member} is not in a voice channel. deafening is unnecessary.")
                return
            #check if the user is already deafened
            if member.voice.deaf:
                await u.send_response(self.bot, ctx, f"{member} is already deafened.")
                return
            
            await member.edit(deafen=True)
            await u.send_response(self.bot, ctx, f"Deafened {member}")

        except Exception as e:
            await u.send_response(self.bot, ctx, "An error occured while trying to deafen the user.")
            print(f"Error in deafen: {e}")
    
    #unmute function - Unmute a user
    @commands.command(name="unmute", 
                      help="Unmute a member in voice",
                      description="""Unmutes a user so they can speak once again.
                      
                      Required Permissions:
                      - Mute Members""",
                      usage="[user]",
                      aliases=["um"])
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self, ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await u.send_response(self.bot, ctx, "Error: You didn't input a user to unmute.")
            return
        
        try:
            #check if the user is already unmuted
            if not member.voice.mute:
                await u.send_response(self.bot, ctx, f"{member} is already unmuted.")
                return

            await member.edit(mute=False)
            await u.send_response(self.bot, ctx, f"Unmuted {member}")

        except Exception as e:
            await u.send_response(self.bot, ctx, "An error occured while trying to unmute the user.")
            print(f"Error in unmute: {e}")
    
    #Undeafen function - Undeafens a user
    @commands.command(name="undeafen", 
                      help="Undeafen a member in voice",
                      description="""Undeafens a user so they can hear others once again.
                      
                      Required Permissions:
                      - Deafen Members""",
                      usage="[user]",
                      aliases=["ud"])
    @commands.has_guild_permissions(deafen_members=True)
    async def undeafen(self, ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await u.send_response(self.bot, ctx, "Error: You didn't input a user to undeafen.")
            return
        
        try:
            #check if the user is already undeafened
            if not member.voice.deaf:
                await u.send_response(self.bot, ctx, f"{member} is already undeafened.")
                return
            
            await member.edit(deafen=False)
            await u.send_response(self.bot, ctx, f"Undeafened {member}")

        except Exception as e:
            await u.send_response(self.bot, ctx, "An error occured while trying to undeafen the user.")
            print(f"Error in undeafen: {e}")
    
    #silence function - Mutes and deafens a user if they are in voice
    @commands.command(name="silence", 
                      help="Mutes and Deafens a member in voice.",
                      description="""Mutes and Deafens a user in voice. 
                      Enjoy the silence!
                      
                      Required Permissions:
                      - Deafen Members
                      - Mute Members""",
                      usage="[user]",
                      aliases=["sil"])
    @commands.has_guild_permissions(deafen_members=True, mute_members=True)
    async def silence(self, ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await u.send_response(self.bot, ctx, "Error: You didn't input a user to silence.")
            return

        try:
            #if the user is not in voice chat, send error message and return
            if member.voice is None:
                await u.send_response(self.bot, ctx, f"{member} is not in a voice chat, silencing them is unecessary.")
                return
            
            #check if the user is already silenced
            if member.voice.deaf and member.voice.mute:
                await u.send_response(self.bot, ctx, f"{member} is already silenced.")
                return
            
            #check if the user is already muted but not deafened
            if member.voice.mute and not member.voice.deaf:
                await member.edit(deafen=True)
                await u.send_response(self.bot, ctx, f"{member} was already muted but not deafened - I've deafened them.")
                return
            
            #check if the user is already deafened but not muted
            if member.voice.deaf and not member.voice.mute:
                await member.edit(mute=True)
                await u.send_response(self.bot, ctx, f"{member} was already deafened but not muted - I've muted them.")
                return
            
            await member.edit(mute=True, deaf=True)
            await u.send_response(self.bot, ctx, f"{member} has been silenced.")
        
        except Exception as e:
            await u.send_response(self.bot, ctx, "An error occured while trying to silence the user.")
            print(f"Error in silence: {e}")
    
    #unsilence function - Unmutes and undeafens a user
    @commands.command(name="unsilence", 
                      help="Unmutes and Undeafens a member in voice",
                      description="""Unmutes and undeafens a user. 
                      if you feel like a user has been silent for too long.
                      
                      Required Permissions:
                      - Deafen Members
                      - Mute Members""",
                      usage="[user]",
                      aliases=["usil", "unsil", "us"])
    @commands.has_guild_permissions(deafen_members=True, mute_members=True)
    async def unsilence(self, ctx, member: discord.Member = None):
        #if no member paramter is entered, return an error message and quit.
        if member is None:
            await u.send_response(self.bot, ctx, "Error: You didn't input a user to unsilence.")
            return
        
        try:
            #check if the user is already unsilenced
            if not member.voice.deaf and not member.voice.mute:
                await u.send_response(self.bot, ctx, f"{member} isn't muted or deafened.")
                return
            
            #Check if the user is muted but not deafened
            if member.voice.mute and not member.voice.deaf:
                await member.edit(mute=False)
                await u.send_response(self.bot, ctx, f"{member} was unmuted. {member} wasn't deafened to begin with.")
                return

            #Check if the user is deafened but not muted
            if member.voice.deaf and not member.voice.mute:
                await member.edit(deafen=False)
                await u.send_response(self.bot, ctx, f"{member} was undeafened. {member} wasn't muted to begin with.")
                return

            await member.edit(mute=False, deafen=False)
            await u.send_response(self.bot, ctx, f"{member} was unsilenced. They can speak and hear again!")

        except Exception as e:
            await u.send_response(self.bot, ctx, "An error occured while trying to unsilence the user.")
            print(f"Error in unsilence: {e}")
    
    #Set response channel - Function to let admins/moderators set a channel for the bot to respond in.
    #One way to contain the bot messages to one place rather than it replying in every channel.
    @commands.command(name="setchannel", 
                      help="Set which channel the bot should respond to.",
                      description="""Set the channel the bot should respond in.
                      By default the bot will respond in the channel a command is sent in.
                      If you change the channel, the bot will ping the user that issued the command.*
                      
                      However, if the user can't see the channel in question, the bot will respond in the same channel the command was issued.
                      if you want to clear the channel the bot responds in, just send the command without any arguments
                      
                      Required Permissions:
                      - Administrator""",
                      usage="[channel]",
                      aliases=["respondhere", "sc"])
    @commands.has_guild_permissions(administrator=True)     #Can be set to any other moderating permission. Remember to change description.
    async def set_response_channel(self, ctx, channel: commands.TextChannelConverter = None):
        try:
            #load existing config
            try:
                with open("config.json", "r") as config_file:
                    config = json.load(config_file)
            except (FileNotFoundError, json.JSONDecodeError):
                config = {}

            #If no channel is provided, clear any stored ID if there is any
            if channel is None:
                if "response_channel_id" in config:
                    config = {}
                    with open("config.json", "w") as config_file:
                        json.dump(config, config_file, indent=4)
                    await u.send_response(self.bot, ctx, "Response channel cleared - I'll respond in whatever channel a command is issued")
                else:
                    await u.send_response(self.bot, ctx, "Response channel is already cleared.")
            else:
                config = {"response_channel_id": channel.id}
                with open("config.json", "w") as config_file:
                    json.dump(config, config_file, indent=4)

                await u.send_response(self.bot, ctx, f"Response channel set to {channel.mention}")
        except Exception as e:
            await ctx.send(f"An error occured: {str(e)}")

    #Rules function - Function to display rules in chat.
    @commands.command(name="rules", 
                      help="Displays the rules of the server",
                      description="""Display the rules of the server.
                      
                      No Permissions needed""")
    async def show_rules(self, ctx):
        #load up config to retreive rules.
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {"rules": "No rules to speak of - Just behave.\nAsk a moderator or admin if you're unsure about something."}

        await u.send_response(self.bot, ctx, config["rules"])

    @commands.command(name="setgreeting",
                      help="Sets welcome message",
                      description="""Allows someone with the proper permissions to change the bot's welcome message.
                      You can leave the message empty if you only use the command on its' own - The bot will confirm if you wish to do so.

                      Required Permissions:
                      - Manage Messages""",
                      usage="[new message]",
                      aliases=["setmsg", "setwelcome", "greeting", "welcome"])
    @commands.has_guild_permissions(manage_messages=True)    #set permissions to administrator or manage_messages depending on who should be able to change the message
    async def set_greeting(self, ctx, msg: str = None):
        #Load up the config file
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {}
            
        #check function for if the message is empty
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n"]
        
        if msg is None:

            await u.send_response(f"Do you want to set the welcome message to be empty?\nReply with a 'Y' for yes or any other input to cancel")
            try:
                response = await self.bot.wait_for('message', check=check, timeout=30.0)
                if response.content.lower() == "y":
                    config["empty_message"] = True
                    config["welcome_message"] = ""      #Save an empty string to wipe any previous message.
                    with open("config.json", "w") as file:
                        json.dump(config, file)
                    await u.send_response(self.bot, ctx, f"Welcome message set to be empty.\nI'll only welcome users with: Welcome to {ctx.guild.name}, <new user>!")
                    return
                else: 
                    await u.send_response(self.bot, ctx, "Interaction cancelled - No new welcome message saved.")
            except TimeoutError:
                await u.send_response(self.bot, ctx, "Time's up - No new welcome message saved.")
                return
        
        #If a message is provided, save it to the config variable and save it to the file.
        #strip any leading or trailing whitespace before saving it

        msg = msg.strip()
        config["welcome_message"] = msg
        config["empty_message"] = False

        with open("config.json", "w") as file:
            json.dump(config, file)

        await u.send_response(self.bot, ctx, 
                              f"""Welcome message updated succesfully!
                              I'll now display this message when a new user joins the server:
                              Welcome to {ctx.guild.name}, <new user>!
                              {msg}""")

    @commands.command(name="setrules",
                      help="Set the rules for the server",
                      description="""Allows someone with the correct permissions to set up new rules that are displayed with !rules 
                      
                      Required Permissions:
                      - Manage Messages""",
                      usage="[new rules]")
    @commands.has_guild_permissions(manage_messages=True)
    async def new_rules(self, ctx, msg: str = None):
        #Load up the config file
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {}

        #check to see if message is empty
        if msg is None:
            config["rules"] = f"No rules to speak of - Just behave.\nAsk a moderator or admin if you're unsure about something."
            with open("config.json", "w") as file:
                json.dump(config, file)
            await u.send_response(self.bot, ctx, 
                                  """Rules set to be generic:
                                  No rules to speak of - Just behave.
                                  just ask a moderator or admin if you're unsure about something.""")
            return
        
        #strip any white space.
        msg = msg.strip()
        config["rules"] = msg
        with open("config.json", "w") as file:
            json.dump(config, file)
        await u.send_response(self.bot, ctx, 
                              f"""Rules updated succesfully! Here's the new rules you've set:
                              {msg}""")

    
async def setup(bot):
    await bot.add_cog(Moderation(bot))