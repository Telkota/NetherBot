import json
import random
import re
import commands.utils as u
from datetime import datetime
from discord.ext import commands


#find the highest int value of ID in quotes
def get_highest_id(quotes):
    if not quotes:
        return 0
    return max(int(quote['id']) for quote in quotes)

def format_quote(quote):
    #break up the quote into variables for readability and ease of use
    nickname = quote['user']['nickname']
    username = quote['user']['username']
    date = quote['date']
    quote_body = quote['quote']
    quote_id = quote['id']

    #to not break the formatting, add "> " after any new line in the quote
    quote_body = quote_body.replace("\n", "\n> ")

    formatted_quote = (f"> **{nickname}** ({username})\n"
                       f"> *on {date}*\n"
                       f"> \n"
                       f"> {quote_body}\n"
                       f"> \n"
                       f"> ID:  `{quote_id}`")
    
    return formatted_quote

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #function to add quotes - a user can reply to a message they want to add as a quote, or write out their own quote
    @commands.command(name="addquote", help="Add a quote to the database")
    async def add_quote(self, ctx, *, quote: str = None):
        #if nothing is provided and the message isn't replying to another message
        if ctx.message.reference is None and quote is None:
            await u.send_response(self.bot, ctx, "Please provide a quote or reply to a message to add it to quotes")
            return

        #Capture the message being replied to
        if ctx.message.reference is not None:
            referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = referenced_message.author
            nickname = user.display_name or user.name       #use nickname if available, otherwise use the username
            username = user.name

            #Check if the reply is to an image
            if referenced_message.attachments:
                image_url = referenced_message.attachments[0].url
                quote = f"{image_url}"
            else:
                quote = referenced_message.content
        #If it's not a reply and the user has provided some text
        else:
            user = ctx.message.author
            nickname = user.display_name or user.name       #use nickname if available, otherwise use the username
            username = user.name

        # remote custom emojis as the bot can't use those
        quote = re.sub(r'<:\w+:\d+>', '', quote)

        #reformat the date to DD/MM/YYYY
        formatted_date = ctx.message.created_at.strftime("%d/%m/%Y")

        #load up exisiting quotes
        try:
            with open("quotes.json", "r+") as file:
                quotes = json.load(file)
        #in case there is no file or an empty file
        except (FileNotFoundError, json.JSONDecodeError):
            quotes = []
        
        #find highest ID and increment it by 1
        highest_id = get_highest_id(quotes)
        new_id = highest_id + 1
        
        #save the quote in a dictionary for inserting into quotes.json
        new_quote = {
            "id": str(new_id),
            "user": {"nickname": nickname, "username": username},
            "quote": quote,
            "date": formatted_date
        }

        #append the new quote and write back to the file
        quotes.append(new_quote)
        with open("quotes.json", "w") as file:
            json.dump(quotes, file, indent=4)

        await u.send_response(self.bot, ctx, f"Quote added!\nID: {new_quote['id']}")

    #function to fetch a random quote from the json file
    @commands.command(name="rquote", help="Get a random quote")
    async def get_quote(self, ctx):
        try:
            with open("quotes.json", "r") as file:
                quotes = json.load(file)
                #if there is any quotes on file
                if quotes:
                    quote = random.choice(quotes)
                    await u.send_response(self.bot, ctx, format_quote(quote))
                else:
                    await u.send_response(self.bot, ctx, f"No quotes available.\nBe on the look out for cool or funny things to quote!")
        except FileNotFoundError:
            await u.send_response(self.bot, ctx, "No quotes available.")
    
    #function to delete a quote - Someone with the correct permissions can delete a quote.
    @commands.command(name="delquote", help="Delete a quote. Either by ID, or by default the latest")
    @commands.has_permissions(manage_messages=True)   #change this to the desired permission. administrator=True or manage_message=True
    async def delete_quote(self, ctx, quote_id: str = None):
        try:
            with open("quotes.json", "r+") as file:
                quotes = json.load(file)

                #If no ID is provided, default to the latest quote
                if quote_id is None:
                    highest_id = get_highest_id(quotes)
                    quote_id = str(highest_id)
                #filter out quotes to find the correct
                quotes = [quote for quote in quotes if quote["id"] != quote_id]

                file.seek(0)
                file.truncate()
                json.dump(quotes, file, indent=4)

            await u.send_response(self.bot, ctx, f"Quote with ID {quote_id} has been deleted.")
        except FileNotFoundError:
            await u.send_response(self.bot, ctx, "No quotes available to delete.")
    
    @commands.command(name="quote", help="Get a quote based on its ID")
    async def get_quote_by_id(self, ctx, quote_id: str = None):
        if quote_id is None:
            await u.send_response(self.bot, ctx, "Please provide a quote ID.")
            return
        
        #load up the file to find the quote
        try:
            with open("quotes.json", "r") as file:
                quotes = json.load(file)
                for quote in quotes:
                    if quote["id"] == quote_id:
                        await u.send_response(self.bot, ctx, format_quote(quote))
                        return
                #if no quote by that ID is found, report back to the user
                await u.send_response(self.bot, ctx, f"No quote found with the ID {quote_id}.")
        except FileNotFoundError:
            await u.send_response(self.bot, ctx, "No quotes available.")
                
async def setup(bot):
    await bot.add_cog(Quotes(bot))