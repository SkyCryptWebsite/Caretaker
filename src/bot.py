import os
import nextcord
import requests
import json
import re
from nextcord.ext import commands
from dotenv import load_dotenv


load_dotenv()

bot = commands.Bot()
TESTING_GUILD_ID = 1125840466366189598


@bot.event
async def on_ready():
    print(f'Login as {bot.user} successful!')

@bot.slash_command(description="Queries the SkyCrypt Knowledgebase!", guild_ids=[TESTING_GUILD_ID])
async def sky(interaction: nextcord.Interaction,query: str):
    await interaction.response.send_message(f"You said: {query}")

bot.run(os.getenv('DISCORD_TOKEN'))