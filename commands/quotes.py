import json
import random
import string
from datetime import datetime
from discord.ext import commands
from commands.utils import get_response_channel

#generator for a short ID to attach to quotes
def generate_id(length=8):
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #function for sending responses
    async def send_response(self, ctx, message):
        response_channel = get_response_channel(self.bot)
        if response_channel is None:
            response_channel = ctx.channel
        await response_channel.send(message)

    #function to add quotes - a user can reply to a message they want to add as a quote, or write out their own quote
    @commands.command(name="addquote", help="Add a quote by replying to someone with !addquote. Alternatively add in your own quote")
    async def add_quote(self, ctx, *, quote: str = None):
        #if nothing is provided and the message isn't replying to another message
        if ctx.message.reference is None and quote is None:
            await self.send_response(ctx, "Please provide a quote or reply to a message to add it to quotes")
            return

        #Capture the message being replied to
        if ctx.message.reference is not None:
            referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = referenced_message.author
            #Check if the reply is to an image
            if referenced_message.attachments:
                image_url = referenced_message.attachments[0].url
                quote = f"Image: {image_url}"
            else:
                quote = referenced_message.content
        #If it's not a reply and the user has provided some text
        else:
            user = ctx.message.author

        #reformat the date to DD/MM/YYYY HH:MM
        formatted_date = ctx.message.created_at.strftime("%d/%m/%Y %H:%M")

        #load up exisitng quotes to check for duplicate IDs
        try:
            with open("quotes.json", "r+") as file:
                quotes = json.load(file)
        except FileNotFoundError:
            quotes = []
        
        #generate a unique ID for the quote
        existing_ids = {quote["id"] for quote in quotes}
        new_id = generate_id()
        while new_id in existing_ids:
            new_id = generate_id()
        
        #save the quote in a dictionary for inserting into quotes.json
        new_quote = {
            "id": new_id,
            "user": str(user),
            "quote": quote,
            "date": formatted_date
        }

        #load up the quotes.json file and insert the quote
        try:
            with open("quotes.json", "r+") as file:
                quotes = json.load(file)            #loading of exisitng quotes
                quotes.append(new_quote)            #append the new quote
                file.seek(0)                        #move file pointer to the start
                json.dump(quotes, file, indent=4)   #write updated quotes back to the file
        except FileNotFoundError:
            with open("quotes.json", "w") as file:
                json.dump([new_quote], file, indent=4)

        await self.send_response(ctx, f"Quote added! ID: {new_quote['id']}")

    #function to fetch a random quote from the json file
    @commands.command(name="rquote", help="Get a random quote")
    async def get_quote(self, ctx):
        try:
            with open("quotes.json", "r") as file:
                quotes = json.load(file)
                #if there is any quotes on file
                if quotes:
                    quote = random.choice(quotes)
                    await self.send_response(ctx, f"on {quote['date']}, {quote['user']} shared:\n"
                                   f"{quote['quote']}\nID: {quote['id']}")
                else:
                    await self.send_response(ctx, f"No quotes available.\nBe on the look out for cool or funny things to quote!")
        except FileNotFoundError:
            await self.send_response(ctx, "No quotes available.")
    
    #function to delete a quote - Someone with the correct permissions can delete a quote.
    @commands.command(name="delquote", help="Delete a quote by its ID")
    @commands.has_permissions(manage_messages=True)   #change this to the desired permission. administrator=True or manage_message=True
    async def delete_quote(self, ctx, quote_id: str = None):
        if quote_id is None:
            await self.send_response(ctx, "you need to provide a quote ID.")
            return
        try:
            with open("quotes.json", "r+") as file:
                quotes = json.load(file)
                quotes = [quote for quote in quotes if quote["id"] != quote_id]
                file.seek(0)
                file.truncate()
                json.dump(quotes, file, indent=4)
            await self.send_response(ctx, f"Quote with ID {quote_id} has been deleted.")
        except FileNotFoundError:
            await self.send_response(ctx, "No quotes available to delete.")
    
    @commands.command(name="quote", help="Get a quote based on its ID")
    async def get_quote_by_id(self, ctx, quote_id: str = None):
        if quote_id is None:
            await self.send_response(ctx, "Please provide a quote ID.")
            return
        
        #load up the file to find the quote
        try:
            with open("quotes.json", "r") as file:
                quotes = json.load(file)
                for quote in quotes:
                    if quote["id"] == quote_id:
                        await self.send_response(ctx, f"On {quote['date']}, {quote['user']} shared:\n"
                                       f"{quote['quote']}\nID: {quote['id']}")
                        return
                #if no quote by that ID is found, report back to the user
                await self.send_response(ctx, f"No quote found with the ID {quote_id}.")
        except FileNotFoundError:
            await self.send_response(ctx, "No quotes available.")
                
async def setup(bot):
    print("Quotes bot setup called")
    await bot.add_cog(Quotes(bot))