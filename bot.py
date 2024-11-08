import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

#grab token from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# bot needs message and members intents in the developer portal
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


#on startup message in console
@bot.event
async def on_ready():
    print(f"\n{bot.user} is connected to the following guild:")
    for guild in bot.guilds:
        print(f"server name: {guild.name} (id: {guild.id})\n")

#Import commands from other modules
from commands import welcome, moderation

#Add commands to bot
welcome.setup(bot)
moderation.setup(bot)


#Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used. Please check the command and try again.")
    else:
        #handle other errors that may occur
        await ctx.send("An error occurred while processing the command.")

bot.run(TOKEN)
