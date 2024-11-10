import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Welcome message
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Welcome to {member.guild.name}, {member.mention}!\n"
                               "No specific rules to mention.\n"
                               "If you have any questions, feel free to DM any officer/admin!")

async def setup(bot):
    await bot.add_cog(Welcome(bot))