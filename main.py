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

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.title_input.value,
            description=self.body.value,
            color=0x045DA0
        )
        embed.set_footer(text="Axie | Cisco NetConnect PUP - Manila")
        await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="announce-axie", description="Send an announcement via modal")
@app_commands.checks.has_permissions(administrator=True)
async def announce(interaction: discord.Interaction):
    await interaction.response.send_modal(AnnounceModal())

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv("DISCORD_TOKEN"))
