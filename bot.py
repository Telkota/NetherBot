import os
import discord
import logging
import traceback
import asyncio
from commands.utils import get_response_channel
from discord.ext import commands
from dotenv import load_dotenv

#setup logging
logging.basicConfig(level=logging.INFO)

#grab token from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# bot needs message and members intents in the developer portal
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

class NetherBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents, help_command=None)
    
    async def load_cogs(self):
        cogs = ["commands.moderation", "commands.quotes", "commands.welcome", "commands.channel_manager", "commands.help"]
        try:
            for cog in cogs:
                await self.load_extension(cog)
                logging.info(f"{cog} loaded succesfully")
        except Exception as e:
            logging.error(f"Error in loading cogs: {e}")

    async def setup_hook(self):
        await self.load_cogs()
    
    async def on_ready(self):
        logging.info(f"Logged in as {self.user.name}")
        print(f"{self.user} is connected to the following guilds:")
        for guild in self.guilds:
            print(f"server name: {guild.name} (id: {guild.id})")

    #Error Responsing
    async def send_error_response(self, ctx, message):
        response_channel = get_response_channel(self)
        if response_channel is None:
            response_channel = ctx.channel
        await response_channel.send(message)

    #Error Handling
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await self.send_error_response(ctx, f"Invalid command. Please check the command and try again.\n"
                                                 "If you don't know what commands I have you can check out `!help` to get a list of commands")
        elif isinstance(error, commands.MissingPermissions):
            await self.send_error_response(ctx, "You don't have the required permissions to run this command. ")
        else:
            #Log the error details in the console
            logging.error(f"An error occured: {error}")
            traceback.print_exception(type(error), error, error.__traceback__)
            
            #Send an error message in Discord
            await self.send_error_response(ctx, f"An error occurred while processing the command:\n"
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
