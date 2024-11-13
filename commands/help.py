import discord
from discord.ext import commands
import utility.utils as u

#Mapping for more user-friendly type names
type_names = {
    str: "String",
    int: "Integer",
    float: "Float",
    bool: "Boolean", 
    discord.Member: "Username (String)",
    commands.TextChannelConverter: "String",
    discord.abc.GuildChannel: "String"
    #Add more as needed
}

#Custom help class to present commands better than the default.
class CustomHelp(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__()

    #function to display all commands available in the bot
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Bot Commands", description="Here are the available commands:", color=discord.Color.blue())
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                formatted_cog_name = cog_name.replace("_", " ")         #remove any underscores and replace it with space
                embed.add_field(name=formatted_cog_name, value="\n".join(command_signatures), inline=False)
        await u.send_response(self.context.bot, self.context, embed)
    
    #function to show more information on certain commands
    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Help with `{command.name}`", description=command.description or "No description available", color=discord.Color.blurple())
        embed.add_field(name="Usage", value=f"`{self.get_command_signature(command)}`", inline=False)
        if command.aliases:         #if there is aliases on a command
            embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)
        if command.clean_params:
            param_str = "\n".join([
                f"- **{name}**: {type_names.get(param.annotation, 'Unknown')}"   #custom type names
                for name, param in command.clean_params.items()
                 ])
            embed.add_field(name="Arguments", value=param_str or "No arguments available.", inline=False)
        
        await u.send_response(self.context.bot, self.context, embed)

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = CustomHelp()

async def setup(bot):
    await bot.add_cog(HelpCog(bot))