import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "Axie is running!"

@app.route("/health")
def health():
    return "OK"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class ChannelSelect(discord.ui.Select):
    def __init__(self, channels):
        options = [
            discord.SelectOption(label=ch.name, value=str(ch.id))
            for ch in channels
        ]
        super().__init__(placeholder="Select a channel...", options=options)

    async def callback(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(int(self.values[0]))
        await interaction.response.send_modal(AnnounceModal(channel))

class ChannelView(discord.ui.View):
    def __init__(self, channels):
        super().__init__(timeout=60)
        self.add_item(ChannelSelect(channels))

class AnnounceModal(discord.ui.Modal, title="New Announcement"):
    title_input = discord.ui.TextInput(
        label="Title",
        placeholder="Announcement title...",
        style=discord.TextStyle.short,
        required=True,
        max_length=256
    )
    body = discord.ui.TextInput(
        label="Body",
        placeholder="Write your announcement here...",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=4000
    )

    def __init__(self, channel: discord.TextChannel):
        super().__init__()
        self.channel = channel

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.title_input.value,
            description=self.body.value,
            color=0x045DA0
        )
        embed.set_footer(text="Axie | Cisco NetConnect PUP - Manila")
        await self.channel.send(embed=embed)
        await interaction.response.send_message(f"Announcement sent to {self.channel.mention}", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="announce-axie", description="Send an announcement via modal")
@app_commands.checks.has_permissions(administrator=True)
async def announce(interaction: discord.Interaction):
    channels = [ch for ch in interaction.guild.text_channels if ch.permissions_for(interaction.guild.me).send_messages]
    await interaction.response.send_message("Where should I send the announcement?", view=ChannelView(channels), ephemeral=True)

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv("DISCORD_TOKEN"))
