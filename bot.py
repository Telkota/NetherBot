import os
import discord
import logging
import traceback
import asyncio
import utility.utils as u
from utility.cog_loader import load_cogs
from discord.ext import commands
from dotenv import load_dotenv

#setup logging
logging.basicConfig(level=logging.INFO)

#grab token from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")

# bot needs message and members intents in the developer portal
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

class NetherBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents, help_command=None)
        self.owner_id = OWNER_ID

    #initial setup of commands
    async def setup_hook(self):
        await load_cogs(self)
    
    async def on_ready(self):
        logging.info(f"Logged in as {self.user.name}")
        print(f"{self.user} is connected to the following guilds:")
        for guild in self.guilds:
            print(f"server name: {guild.name} (id: {guild.id})")

    #Error Handling
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await u.send_response(self, ctx, f"Invalid command. Please check the command and try again.\n"
                                                 "If you don't know what commands I have you can check out `!help` to get a list of commands")
        elif isinstance(error, commands.MissingPermissions):
            await u.send_response(self, ctx, "You don't have the required permissions to run this command. ")
        else:
            #Log the error details in the console
            logging.error(f"An error occured: {error}")
            traceback.print_exception(type(error), error, error.__traceback__)
            
            #Send an error message in Discord
            await u.send_response(self, ctx, f"An error occurred while processing the command:\n"
                        f"{error}")


async def main():
    bot = NetherBot()

    #try-except block for handling shutdowns through keyboard interruption
    try:
        async with bot:
            await bot.start(TOKEN)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logging.info("Bot is shutting down doe to keyboard interruption...")
        await bot.close()
    finally:
        logging.info("Bot has been closed cleanly. Hopefully.")

if __name__ == "__main__":
    asyncio.run(main())
