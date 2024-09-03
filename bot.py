import subprocess
import sys

# Check if discord module is installed, install if not
try:
    import discord
    from discord.ext import commands
except ImportError:
    print("Discord module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "discord.py"])
    import discord
    from discord.ext import commands

# Initialize the bot with the command prefix and enable intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='', intents=intents)  # Changed command_prefix from '/' to ''

# Define the mdel command
@bot.command(name='mdel')  # Changed from /mdel to mdel
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

# Run the bot with your token
bot.run('')
