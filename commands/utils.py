import json

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
async def send_response(bot, ctx, message):
    response_channel = get_response_channel(bot)
    #try-except just in case something happens
    try:
        #If the user don't have permission to view the response channel, then send response in whatever channel they submitted the command in
        if response_channel is None or not response_channel.permissions_for(ctx.author).read_messages:
            response_channel = ctx.channel

        #Don't mention the user if the command is sent in the same channel as the response channel
        if response_channel.id == ctx.channel.id:
            await response_channel.send(message)
        else:
            user_mention = ctx.author.mention
            await response_channel.send(f"{user_mention} - {message}")
    except Exception as e:
        await ctx.channel.send(f"An error occured while sending the response. {e}")