import logging
import os
from discord.ext import commands

async def load_cogs(bot: commands.Bot, cog_file: str = None):
    if cog_file is None:
        base_directory = os.path.dirname(os.path.abspath(__file__))
        cog_file = os.path.join(base_directory, "cogs.list")
    try:
        #read the cogs from the cogs file
        with open(cog_file, "r") as file:
            cogs = [line.strip() for line in file if line.strip()]
        
        for cog in cogs:
            try:
                if cog in bot.extensions:
                    await bot.reload_extension(cog)
                    logging.info(f"{cog} reloaded successfully")
                else:
                    await bot.load_extension(cog)
                    logging.info(f"{cog} loaded successfully")
            except Exception as e:
                logging.error(f"Error loading {cog}: {e}")
    except FileNotFoundError:
        logging.error(f"The file '{cog_file}' does not exist")
    except Exception as e:
        logging.error(f"An error occurred while loading cogs: {e}")
                