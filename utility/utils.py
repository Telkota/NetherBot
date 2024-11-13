import json
import discord

#Utility script. fetches the response channel id from the config file if it has been set
def get_response_channel(bot):
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            channel_id = config.get("response_channel_id")
            if channel_id:
                return bot.get_channel(channel_id)
    except FileNotFoundError:
        pass
    return None

#function for sending responses
async def send_response(bot, ctx, message, delete_after=None):
    response_channel = get_response_channel(bot)
    #try-except just in case something happens
    try:
        #If the user don't have permission to view the response channel, then send response in whatever channel they submitted the command in
        if response_channel is None or not response_channel.permissions_for(ctx.author).read_messages:
            response_channel = ctx.channel

        #Check if the message is an embed
        if isinstance(message, discord.Embed):
            sent_message = await response_channel.send(embed=message, delete_after=delete_after)
        else:
            #check whether the response channel is the same as the channel the command is sent in
            user_mention = ctx.author.mention if response_channel.id != ctx.channel.id else ""
            sent_message = await response_channel.send(f"{message} {user_mention}", delete_after=delete_after)

        #return sent_message statement to make delete_messages work (channel_manager.py)
        return sent_message
    
    except Exception as e:
        await ctx.channel.send(f"An error occured while sending the response. {e}")
        return None