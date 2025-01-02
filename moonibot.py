import discord
from discord import app_commands
from discord.ext import commands

# Replace with your bot token
TOKEN = "MTMyMjY2NzA4NTEzNzk2OTMwMw.GwJWJK.hHlHLC_NvJSynY24n5aM3pz-4cjg9Lmvbg5iIo"

# Replace with your server ID and channel ID
SERVER_ID = 1321149043732381778  # Replace with current server ID
CHANNEL_ID = 91321249693920923648  # Replace with current channel ID

# Initialize the bot with the necessary intents
intents = discord.Intents.default()
intents.message_content = True
class Moonibot(commands.Bot):
    def __init__(self, *, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self) -> None:
        # Sync the commands to the server
        guild = discord.Object(id=SERVER_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        await bot.tree.sync()

bot = Moonibot(command_prefix='/', intents=intents)

class Moonibot(commands.Bot):
    def __init__(self, *, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self) -> None:
        # Sync the commands to the server
        guild = discord.Object(id=SERVER_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        await bot.tree.sync()


# Output to the console that the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print("Successfully started up.")
    print('------')

#Creates a dm with the user

@bot.tree.command(name="dm", description="Create a direct message with the bot.")
@app_commands.guild_only()
async def dm(interaction: discord.Interaction):
    await interaction.response.send_message("Check your DMs!", ephemeral=True)
    await interaction.user.send("Hello! This is a DM from Moonibot. How can I help you?")

# Help command
@bot.tree.command(name="help", description="Get help on using the bot.")
@app_commands.command()
async def help(interaction: discord.Interaction):
    if not isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message("This command can only be used in DMs.", ephemeral=True)
        return

    help_message = """
    **Moonibot Help**

    **/help**: Displays this help message.
    **/send_link**: Sends a link to a specific channel.
    **/send_video**: Sends a video to a specific channel.

    **Note:** All commands must be used in DMs with the bot.
    """
    await interaction.response.send_message(help_message, ephemeral=False)

# Send link command with modal
@bot.tree.command(name="send_link", description="Send a link to a specific channel.")
@app_commands.command()
async def send_link(interaction: discord.Interaction):
    if not isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message("This command can only be used in DMs.", ephemeral=True)
        return

    class LinkModal(discord.ui.Modal, title='Submit a Link'):
        link = discord.ui.TextInput(
            label='Link',
            placeholder='Enter your link here',
            style=discord.TextStyle.short,
        )

        async def on_submit(self, interaction: discord.Interaction):
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(self.link.value)
            await interaction.response.send_message(f"Link sent to {channel.mention}!", ephemeral=True)

    await interaction.response.send_modal(LinkModal())

# Send video command
@bot.tree.command(name="send_video", description="Send a video to a specific channel.")
@app_commands.command()
async def send_video(interaction: discord.Interaction):
    if not isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message("This command can only be used in DMs.", ephemeral=True)
        return

    await interaction.response.send_message("Please send the video file.", ephemeral=True)

    def check(message):
        return message.author == interaction.user and message.channel == interaction.channel and message.attachments

    try:
        message = await bot.wait_for('message', check=check, timeout=60)
    except TimeoutError:
        await interaction.followup.send("You didn't send a video in time.", ephemeral=True)
        return

    if message.attachments:
        file = message.attachments[0]
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(file=await file.to_file())
        await interaction.followup.send(f"Video sent to {channel.mention}!", ephemeral=True)
    else:
        await interaction.followup.send("No video file found.", ephemeral=True)

# Run the bot
bot.run("MTMyMjY2NzA4NTEzNzk2OTMwMw.GwJWJK.hHlHLC_NvJSynY24n5aM3pz-4cjg9Lmvbg5iIo")
