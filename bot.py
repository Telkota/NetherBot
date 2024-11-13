import os
import discord
import logging
import traceback
import asyncio
import commands.utils as u
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

    #Command to reload cogs for updating the bot without having to shut down the bot.
    @commands.command(name="reload", 
                      description="""Command to refresh the bot's scripts.
                      
                      Required Permissions:
                      - Administrator
                      (command available to bot writer regardless of permissions)
                      """)
    async def reload(self, ctx):
        #Check to see if the user is the bot developer or has administrator permissions
        if ctx.author.id == self.owner_id or ctx.author.guild_permissions.administrator:
            await self.load_cogs()
            await u.send_response(self.bot, ctx, "Cogs reloaded successfully.")
        else:
            await u.send_response(self.bot, ctx, "You don't have permissions to refresh the bot.")


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
