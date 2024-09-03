import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ... (rest of your imports and bot setup)

# Replace the bot.run line with this:
bot.run(os.getenv('DISCORD_BOT_TOKEN'))

# Initialize the bot with the command prefix and enable intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Define the /delete command
@bot.command()
async def mdel(ctx):
    # Check if the user has the 'Manage Messages' permission
    if ctx.author.guild_permissions.manage_messages:
        # Inform the user that the deletion process has started
        await ctx.send("Deleting all messages...")

        # Function to delete messages older than 14 days
        async def delete_old_messages():
            async for message in ctx.channel.history(limit=None, oldest_first=True):
                if (discord.utils.utcnow() - message.created_at).days >= 14:
                    try:
                        await message.delete()
                    except discord.errors.HTTPException:
                        pass

        # Delete messages in bulk for messages less than 14 days old
        deleted = await ctx.channel.purge(limit=None, bulk=True)

        # Inform the user about the number of deleted messages
        await ctx.send(f"Deleted {len(deleted)} messages from the last 14 days. Now deleting older messages...")

        # Delete older messages individually
        await delete_old_messages()

        await ctx.send("All messages have been deleted!")
    else:
        await ctx.send("You do not have the required permissions to use this command.")

# Define the /mfind command
@bot.command()
async def mfind(ctx):
    total_messages = 0
    messages_with_defeat = 0

    # Iterate through the message history in the channel
    async for message in ctx.channel.history(limit=None):
        total_messages += 1
        if "defeat" in message.content.lower():  # Case insensitive search for "defeat"
            messages_with_defeat += 1

    messages_without_defeat = total_messages - messages_with_defeat

    # Send the results to the channel
    await ctx.send(f"Total number of messages in this channel: {total_messages}")
    await ctx.send(f"Total number of messages containing 'defeat': {messages_with_defeat}")
    await ctx.send(f"Total number of messages minus those containing 'defeat': {messages_without_defeat}")

# Run the bot with your token
