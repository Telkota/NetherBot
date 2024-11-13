# NetherBot
 Repo for NetherBot, a discord bot written for Nether Vortex.
 The bot is only really intended to be used in our server.

 This is a hobby project done by Telkota.
 I wanted more experience in coding/programming, and at the same time maybe have something to show off. 

 *As such I haven't really set up any licensing on it, along with it being a project made by a newbie so this project probably ain't the best resource to take from either.*
 
 There's probably some bugs to iron out, and code might be messy and/or confusing.
 I'm not really a confident coder yet and still learning along the way.

 ## Features:
    - Moderation tools
        - Ban users
        - Kick users
        - Mute/Unmute users
        - Deafen/Undeafen users
        - Move a user to a different voice channel
        - Move all users to a specific voice channel
        - Set response channel for the bot (default is the same channel as the command)
        - Silence/Unsilence users (Mutes & Deafens)
        - Display Server Rules
        - Modify the Server Rules message
        - Modify the welcome message
    
    - Channel Management
        - Create new channels (voice and text)
        - Delete Channels
        - Delete recent messages* (Some restrictions apply - check !help delmessages)
    
    - Quotes
        - Reply to a message with !addquote (or an alias) to add the quote to the bot.
        - User can also enter a quote into the bot wiht !addquote <text>
        - Fetch random quote from the bot
        - Fetch a specific quote from the bot by using the ID of the quote
        - Admins/Mods can delete quotes either by ID or latest quote (default)

If you see or encounter any bugs, report them here or to me at discord (Telkota).

 *(For transparency sake: Made with liberal use of Google & Bing's Copilot after a few of months of casually learning Python and javascript.)*

## Versions: 

Ver 1.1 - 13/nov/24
- Added functions to let moderators/admins to change Welcome message and rules
    - Welcome message will always contain a message of "Welcome to <server name>, <new user>!"
    - You can change the welcome message with !setgreeting (or an alias)
    - You can set new rules with !setrules
    - By default it will display a generic rules message. if you only do !setrules it will go back to the default generic rules message.
- Added function to refresh the bot's scripts.
    - Mostly for development purposes. Allows me to update the bot without shutting it down
        - (unless there is changes to the main bot script)

Ver 1.0 - 11/nov/24:
- First full version complete
- Added custom help command
- Cleaned up the code a bit

Ver 0.4 - 10/nov/24:
- Added Channel Management capabilities.
    - Only available to users with certain permissions
    - Create new channels (text or voice)
    - Delete channels
    - Delete messages

Ver 0.3.5 - 10/nov/24:
- Reformatted how the quote is presented
- Simplified the unique IDs for quotes

Ver 0.3 - 08-09/nov/24:
- Added quote capabilities.
    - users can add quotes either by replying to a message or writing something to quote
    - users can fetch a random quote or a specific quote by ID
    - moderators/Admins can delete quotes based on ID

Ver 0.2 - 08/nov/24 :
- Added moderation capabilities
    - Only available to users with certain permissions
    - Kick/ban users
    - Mute/unmute users
    - Deafen/undeafen users
    - Move users between voice channels - Either one at a time or everyone to one channel
    - Silence users (Mute & undeafen) and "unsilence" users

 Ver 0.1 - 07/nov/24 :
 - Made sure the bot can connect to discord. 
 - Welcome message.
