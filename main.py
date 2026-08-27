import os
import discord
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
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, activity=discord.Game(name="Cisco NetConnect PUP - Manila"))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="announce")
@commands.has_permissions(administrator=True)
async def announce(ctx, channel: discord.TextChannel, *, message):
    embed = discord.Embed(description=message, color=0x045DA0)
    embed.set_footer(text="Axie | Cisco NetConnect PUP - Manila")
    await channel.send(embed=embed)
    await ctx.send(f"Announcement sent to {channel.mention}")

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv("DISCORD_TOKEN"))
