import discord
from discord.ext import commands
import os
import openai   # Importing OpenAI for future use

# TOKEN = os.getenv('DISCORD_TOKEN')

# Replace with Mooni's channel IDs
TARGET_CHANNEL_ID = 1331673533834727445 #Mods review channel
APPROVED_CHANNEL_ID = 1331673497662918676 #Channel for approved submissions

# Emoji for reactions
EMOJI_APPROVE = "✅"
EMOJI_REJECT = "❌"

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.tree.sync()  # Sync the commands
    print("successfully finished startup!")

@bot.tree.command(name="help", description="Shows the help message.")  # Renamed to avoid conflict
async def my_help(interaction: discord.Interaction):
    """Shows this help message."""
    await interaction.response.send_message(
        "**Commands (use in DMs):**\n"
        "/send_video - Sends the attached video to the mods review channel.\n"
        "/send_link <link> - Sends the link to the mods review channel.\n"
        "**Commands (use anywhere):**\n"
        "/dm - Sends you a direct message."
    , ephemeral=True)

@bot.tree.command(name="send_video", description="Sends the video to the mods review channel (DM only).")
@commands.dm_only()
async def send_video(interaction: discord.Interaction, video: discord.Attachment):
    """Sends the video to the target channel (DM only)."""
    try:
        if not video.content_type.startswith("video"):
            return await interaction.response.send_message("Please provide a video file.", ephemeral=True)

        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        
        embed = discord.Embed(title="Video Submission", description=f"Sent by {interaction.user.mention}")
        embed.set_footer(text=f"Filename: {video.filename}")
        await target_channel.send(embed=embed, file=await video.to_file())
        
        await interaction.response.send_message("Video sent successfully!", ephemeral=True)

    except discord.HTTPException as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:  # Ignore bot's own reactions
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = bot.get_user(payload.user_id)
    emoji = payload.emoji.name

    if emoji == EMOJI_APPROVE:
        if message.embeds and message.attachments:
            # Send to approved channel
            approved_channel = bot.get_channel(APPROVED_CHANNEL_ID)
            await approved_channel.send(f"Approved video from {message.embeds[0].description}:", 
                                       embed=message.embeds[0], 
                                       files=[await a.to_file() for a in message.attachments])
            await message.delete()
        else:
            await user.send("The message does not have the required embeds or attachments to approve.", ephemeral=True)

    elif emoji == EMOJI_REJECT:
        # Delete the message
        await message.delete()

@bot.tree.command(name="send_link", description="Sends the link to the target channel.") # Register slash command
@commands.dm_only()  # Restrict command to DMs
async def send_link(interaction: discord.Interaction, link: str):
    """Sends the link to the target channel."""
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    await target_channel.send(f"Link sent by {interaction.user.mention}:\n{link}") # Sends message with @mention
    await interaction.response.send_message("Link sent successfully!")

@bot.tree.command(name="dm", description="Sends you a direct message.")  # Register slash command
async def dm(interaction: discord.Interaction):
    """Sends you a direct message."""
    user = interaction.user # Get the user who used the command
    await user.send("'Ello, I'm mooni bot! I can help you send videos and links to mooni's channel. Use the /help command to see the available commands.")
    await interaction.response.send_message("I've sent you a DM", ephemeral=True) 

bot.run("MTMyMjY2NzA4NTEzNzk2OTMwMw.GDssWN.01pfcZJvKTMLiqoKfInMdcLnNSRkr56wrbtrqk")