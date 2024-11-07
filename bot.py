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

#List of channel names to check for welcome message - Switch out or add names as needed
welcome_channel_names = ["social", "general"]

#on startup message in console
@bot.event
async def on_ready():
    print(f"\n{bot.user} is connected to the following guild:")
    for guild in bot.guilds:
        print(f"server name: {guild.name} (id: {guild.id})\n")

#welcome function
@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if channel.name in welcome_channel_names:
            #Send welcome message to the new member in the channel the joined message appears.
            #Edit the message if needed
            await channel.send(f"Welcome to {member.guild.name}, {member.mention}!\n"
                               "No specific rules to mention - Just act like a normal humanbeing and we should be cool\n"
                               "If you have any questions feel free to DM any officer/admin!")


#error handling
@bot.event
async def on_error(event, *args, **kwargs):
    with open("err.log", "a") as f:
        if event == "on_message":
            f.write(f"unhandled message: {args[0]}\n")
        else:
            raise

bot.run(TOKEN)
