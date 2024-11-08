import os
import discord
import logging
import traceback
from discord.ext import commands
from dotenv import load_dotenv

#setup logging
logging.basicConfig(level=logging.ERROR)

#grab token from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# bot needs message and members intents in the developer portal
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


#on startup message in console
@bot.event
async def on_ready():
    print(f"\n{bot.user} is connected to the following guild:")
    for guild in bot.guilds:
        print(f"server name: {guild.name} (id: {guild.id})\n")

        #for testing purposes: Bot Permissions. Remove later
        bot_member = guild.get_member(bot.user.id)
        for channel in guild.channels:
            permissions = channel.permissions_for(bot_member)
            print(f"Channel: {channel.name}, Permissions: {permissions}")

#Import commands from other modules
from commands import welcome, moderation

#Add commands to bot
welcome.setup(bot)
moderation.setup(bot)


#Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Invalid command. Please check the command and try again.\n"
                       "If you don't know what commands I have you can check out `!help` to get a list of commands")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required permissions to run this command. ")
    else:
        #Log the error details in the console
        logging.error(f"An error occured: {error}")
        traceback.print_exception(type(error), error, error.__traceback__)
        
        #Send an error message in Discord
        await ctx.send(f"An error occurred while processing the command:\n"
                       f"{error}")

bot.run(TOKEN)
