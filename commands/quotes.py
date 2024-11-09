import json
import random
import string
from datetime import datetime
from discord.ext import commands

#generator for a short ID to attach to quotes
def generate_id(lenght=8):
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=lenght))

def setup(bot):
    @bot.command(name="addquote", help="Add a quote by replying to someone with !addquote. Alternatively add in ")
    async def add_quote(ctx, *, quote: str = None):
        #if nothing is provided and the message isn't replying to another message
        if ctx.message.reference is None and quote is None:
            await ctx.send("Please provide a quote or reply to a message to add it to quotes")
            return

        #Capture the message being replied to
        if ctx.message.reference is not None:
            referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = referenced_message.author
            #Check if the reply is to an image
            if referenced_message.attachments:
                image_url = referenced_message.attachments[0].url
                quote = f"[Image: {image_url}]"
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

        await ctx.send("Quote added!")

    @bot.command(name="rquote", help="Get a random quote")
    async def get_quote(ctx):
        try:
            with open("quotes.json", "r") as file:
                quotes = json.load(file)
                #if there is any quotes on file
                if quotes:
                    quote = random.choice(quotes)
                    await ctx.send(f"on {quote['date']}, {quote['user']} shared:\n"
                                   f"`{quote['quote']}`\nID: {quote['id']}")
                else:
                    await ctx.send(f"No quotes available.\nBe on the look out for cool or funny things to quote!")
        except FileNotFoundError:
            await ctx.send("No quotes available.")
    
    @bot.command(name="delquote", help="Delete a quote by its ID")
    @commands.has_permissions(manage_messages=True)   #change this to the desired permission. administrator=True or manage_message=True
    async def delete_quote(ctx, quote_id: str = None):
        if quote_id is None:
            await ctx.send("you need to provide a quote ID.")
            return
        try:
            with open("quotes.json", "r+") as file:
                quotes = json.load(file)
                quotes = [quote for quote in quotes if quote["id"] != quote_id]
                file.seek(0)
                file.truncate()
                json.dump(quotes.file, indent=4)
            await ctx.send(f"Quote with ID {quote_id} has been deleted.")
        except FileNotFoundError:
            await ctx.send("No quotes available to delete.")
    
    @bot.command(name="quote", help="Get a quote based on its ID")
    async def get_quote_by_id(ctx, quote_id: str = None):
        if quote_id is None:
            await ctx.send("Please provide a quote ID.")
            return
        
        #load up the file to find the quote
        try:
            with open("quotes.json", "r") as file:
                quotes = json.load(file)
                for quote in quotes:
                    if quote["id"] == quote_id:
                        await ctx.send(f"On {quote['date']}, {quote['user']} shared:\n"
                                       f"`{quote['quote']}\nID: {quote['id']}`")
                        return
                #if no quote by that ID is found, report back to the user
                await ctx.send(f"No quote found with the ID {quote_id}.")
        except FileNotFoundError:
            await ctx.send("No quotes available.")
                