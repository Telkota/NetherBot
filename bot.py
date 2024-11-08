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
from commands import welcome

#Add commands to bot
welcome.setup(bot)


bot.run(TOKEN)
