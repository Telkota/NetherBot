import commands.utils as u
import discord
from discord.ext import commands

class ChannelManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Function to create new channels. 
    @commands.command(name="createchannel", help="Create a new text or voice channel")
    @commands.has_guild_permissions(manage_channels=True)
    async def create_channel(self, ctx, channel_name: str = None, channel_type: str = "text"):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        
        #Check if the user provided a channel name
        if channel_name is None:
            await u.send_response(self.bot, ctx, f"You need to provide a channel name first.\nIf you want a voice channel make sure to add voice after the name")
            return
        
        #Check if the channel already exists
        if existing_channel:
            await u.send_response(self.bot, ctx, f"Channel {channel_name.mention} already exists.")
            return

        #check if the channel type is voice, otherwise create text channel
        if channel_type.lower() == "voice":
            new_channel = await guild.create_voice_channel(channel_name)
            await u.send_response(self.bot, ctx, f"Voice channel {new_channel.mention} created.")
        else:
            new_channel = await guild.create_text_channel(channel_name)
            await u.send_response(self.bot, ctx, f"Text channel {new_channel.mention} created.")

    #Function to delete channels - With confirmation safeguard
    @commands.command(name="delchannel", help="Delete a channel")
    @commands.has_guild_permissions(manage_channels=True)
    async def delete_channel(self, ctx, channel: discord.abc.GuildChannel):
        def check(msg):
            #nested function to do a few checks for the delete_channel function
            #It checks whether the confirmation message comes from the same person that sent the command
            #Also checks if the message is sent in the same channel where the command was sent
            #and it checks whether it contents y or n
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n"]

        await u.send_response(self.bot, ctx, f"Are you sure you want to delete {channel.name}? Type Y to confirm, N to cancel.")

        try:
            #Wait for a message - Timeout 30 sec. 
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)

            #When they've replied, check the message
            if msg.content.lower() == "y":
                await channel.delete()
                await u.send_response(self.bot, ctx, f"Channel '{channel.name}' has been deleted.")
            else:
                await u.send_response(self.bot, ctx, "Channel deletion cancelled.")
        except:
            await u.send_response(self.bot, ctx, "Time's up - Channel deletion cancelled.")

    #Function to delete messages - With confirmation safeguard. 
    #Some limits apply: only up to 100 messages due to API limitations, and only messages within the last 14 days.
    @commands.command(name="delmessages", help="Deletes the x most recent messages*")
    @commands.has_guild_permissions(manage_messages=True)
    async def delete_messages(self, ctx, amount: int):
        if amount < 1:
            await u.send_response(f"Please specify a valid number of messages to delete within {ctx.channel.mention}")
            return
        
        #Confirmation function like in the above function
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n"]

        confirmation_message = await u.send_response(self.bot, ctx, f"Are you sure you want to delete the last {amount} of messages? Type 'Y' to confirm or 'N' to cancel.")
        if confirmation_message is None:
            await u.send_response(self.bot, ctx, "Failed to send the confirmation message")
            return
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)

            #If the user has confirmed - Delete message. 
            if msg.content.lower() == "y":
                await confirmation_message.delete()     #Delete bot question
                await msg.delete()                      #Delete user confirmation
                
                #deletion of the !command message
                async for message in ctx.channel.history(limit=1):
                    await message.delete()

                #deletion of the x amount of messages requested.
                deleted = await ctx.channel.purge(limit=amount)
                await u.send_response(self.bot, ctx, f"Deleted {len(deleted)} messages. This message will be removed in 10 seconds", delete_after=10)
            else:
                await u.send_response(self.bot, ctx, "Message deletion cancelled.")
        except discord.errors.NotFound:
            await u.send_response(self.bot, ctx, "One of the messages was not found, operation cancelled.")
        except discord.errors.Forbidden:
            await u.send_response(self.bot, ctx, "I don't have permission to delete messages here.")
        except discord.errors.HTTPException as e:
            await u.send_response(self.bot, ctx, f"An error occurred: {e}")
        except TimeoutError:
            await u.send_response(self.bot, ctx, "Time's up - Message deletion cancelled.")
        

async def setup(bot):
    await bot.add_cog(ChannelManagement(bot))