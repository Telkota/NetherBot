import discord
from discord.ext import commands

#List of channel names to check for welcome message - Switch out or add names as needed
welcome_channel_names = ["social", "general"]

#welcome function
def setup(bot):
    @bot.event
    async def on_member_join(member):
        for channel in member.guild.channels:
            if channel.name in welcome_channel_names:
                #Send welcome message to the new member in the channel the joined message appears.
                #Edit the message if needed
                await channel.send(f"Welcome to {member.guild.name}, {member.mention}!\n"
                                "No specific rules to mention - Just act like a normal humanbeing and we should be cool\n"
                                "If you have any questions feel free to DM any officer/admin!")
                break
