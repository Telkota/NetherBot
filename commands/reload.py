import discord
import logging
import utility.utils as u
from utility.cog_loader import load_cogs
from discord.ext import commands

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Command to reload cogs for updating the bot without having to shut down the bot.
    @commands.command(name="reload", 
                      description="""Command to refresh the bot's scripts.
                      
                      Required Permissions:
                      - Administrator
                      (command available to bot writer regardless of permissions)
                      """)
    async def reload(self, ctx):
        #Check to see if the user is the bot developer or has administrator permissions
        if ctx.author.id == self.bot.owner_id or ctx.author.guild_permissions.administrator:
            await load_cogs(self.bot)
            await u.send_response(self.bot, ctx, "Cogs reloaded successfully.")
        else:
            await u.send_response(self.bot, ctx, "You don't have permissions to refresh the bot.")

async def setup(bot):
    await bot.add_cog(Reload(bot))