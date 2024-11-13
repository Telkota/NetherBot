import discord
import json
import logging
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Welcome message
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            #Variable to store the base greeting
            welcome_user = f"Welcome to {member.guild.name}, {member.mention}!\n"
            generic_message = "No rules to mention - If you have any questions, feel free to ask any officer/admin!"
            try:
                #Check for existing welcome message within config.json
                with open("config.json", "r") as file:
                    config = json.load(file)
                
                #Add the welcome message into a variable if it exists, if not add a generic message
                welcome_message = config.get("welcome_message", generic_message)

                #If the welcome_message variable is empty, then add in generic_message
                if not welcome_message:
                    welcome_message = generic_message

            except (FileNotFoundError, json.JSONDecodeError):
                welcome_message = generic_message
            
            full_message = welcome_user + welcome_message
            await channel.send(full_message)
            
        else:
            #Log a message if system channel is not found, or the bot doesn't have access.
            print(f"System channel not found or are inaccessible. (Server: {member.guild.name})")

async def setup(bot):
    await bot.add_cog(Welcome(bot))