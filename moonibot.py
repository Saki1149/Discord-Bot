import discord
from discord import app_commands
from discord.ext import commands

# Set up the bot
intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with the name of your target channel
TARGET_CHANNEL_NAME = "mods-review-submissions"

@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync the commands with Discord
    print(f"Logged in as {bot.user} and ready to serve!")
    print(f"Successfully finished startup!")

@bot.tree.command(name="submit_video", description="Submit a video link to the bot")
async def submit_video(interaction: discord.Interaction):
    """
    Slash command that asks the user for a video link and posts it in a specific channel.
    """
    try:
        # Send DM to the user to collect the link
        await interaction.response.send_message("Check your DMs to submit your video link!", ephemeral=True)
        
        user = interaction.user
        dm_channel = await user.create_dm()
        await dm_channel.send("Hi! Please reply with the link to the video you'd like to submit.")

        # Define a check for the message response
        def check(m):
            return m.author == user and m.guild is None

        # Wait for the user's response
        msg = await bot.wait_for('message', check=check, timeout=120)  # 2 minutes to respond

        # Get the target channel
        guild = interaction.guild
        target_channel = discord.utils.get(guild.text_channels, name=TARGET_CHANNEL_NAME)

        if target_channel:
            # Post the video link in the target channel
            await target_channel.send(f"New video submission from {user.name}: {msg.content}")
            await dm_channel.send("Your video has been sent! Thank you!")
        else:
            await dm_channel.send(f"Sorry, I couldn't find the channel `{TARGET_CHANNEL_NAME}`.")
    except discord.Forbidden:
        await interaction.response.send_message("I couldn't send you a DM. Please check your DM settings.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
    except discord.errors.TimeoutError:
        await user.send("You didn't respond in time. Please try again using the `/submit_video` command.")

@bot.tree.command(name="help", description="Get help with Moonibot commands")
async def help_command(interaction: discord.Interaction):
    """
    Slash command to provide help information about Moonibot.
    """
    await interaction.response.send_message("Check your DMs for help!", ephemeral=True)
    user = interaction.user
    dm_channel = await user.create_dm()
    await dm_channel.send("Here are the commands you can use:\n\n"
                          "/submit_video - Submit a video.\n"
                          "/help - Get help with commands.\n\n"
                          "Feel free to reach out for support!")

# Run the bot with your token
bot.run("MTMyMjY2NzA4NTEzNzk2OTMwMw.GwJWJK.hHlHLC_NvJSynY24n5aM3pz-4cjg9Lmvbg5iIo")
