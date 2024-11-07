import os
import discord
from dotenv import load_dotenv

# bot needs message and members intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#grab token from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=intents)

#List of channel names to check for welcome message - Switch out or add names as needed
welcome_channel_names = ["social", "general"]

#on startup message in console
@client.event
async def on_ready():
    print(f"\n{client.user} is connected to the following guild:")
    for guild in client.guilds:
        print(f"server name: {guild.name} (id: {guild.id})\n")

#welcome function
@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if channel.name in welcome_channel_names:
            #Send welcome message to the new member in the channel the joined message appears.
            #Edit the message if needed
            await channel.send(f"Welcome to {member.guild.name}, {member.mention}!\n"
                               "No specific rules to mention - Just act like a normal humanbeing and we should be cool\n"
                               "If you have any questions feel free to DM any officer/admin!")


client.run(TOKEN)
