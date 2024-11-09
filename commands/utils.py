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