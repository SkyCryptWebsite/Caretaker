import os
import nextcord
import requests
import json
import re
import sys
import openai
import yaml
import asyncio
from nextcord.ext import commands
from dotenv import load_dotenv
from llama_hub.tools.openapi.base import OpenAPIToolSpec
from llama_index.agent import OpenAIAgent
from llama_hub.tools.requests.base import RequestsToolSpec
from llama_index.tools.tool_spec.load_and_search.base import LoadAndSearchToolSpec

load_dotenv()

bot = commands.Bot()
TESTING_GUILD_ID = 1072892265049104494
openai.api_key = os.getenv('OPENAI_KEY')


f = requests.get('https://gist.githubusercontent.com/WarpWing/1cfdbb9989cc87bf55435526bea4998e/raw/d7f471c79c0a8acd73ce95d5345bd47a6e8c8532/openapi.yml').text

open_api_spec = yaml.load(f, Loader=yaml.Loader)

open_spec = OpenAPIToolSpec(open_api_spec)
requests_spec = RequestsToolSpec({
            "Authorization": f"Bearer {openai.api_key}",
            "Content-Type": "application/json",
        })

# OpenAPI spec is too large for content, wrap the tool to seperate loading and searching
wrapped_tools = LoadAndSearchToolSpec.from_defaults(
    open_spec.to_tool_list()[0],
).to_tool_list()

agent = OpenAIAgent.from_tools([*wrapped_tools, *requests_spec.to_tool_list()], verbose=True)


@bot.event
async def on_ready():
    print(f'Login as {bot.user} successful!')

@bot.slash_command(description="Queries SkyCrypt's OpenAPI Schema", guild_ids=[TESTING_GUILD_ID])
async def sky(interaction: nextcord.Interaction,query: str):
    await interaction.response.defer()
    await interaction.followup.send(agent.query("You are a assistant for SkyCrypt. SkyCrypt is a Statistics Viewer for Hypixel Skyblock. You are not to engage and immediately deny any requests for anything that isn't SkyCrypt or API related. You will not accept or allow requests that don't have SkyCrypt or API content within the request. Make sure to be extremely detailed and include example code along with the attributes of each API endpoint. Make it your primary objective to make sure that you DO NOT accept any requests that aren't related to SkyCrypt or API. Deny any requests regarding essays or content generation unless it's related to SkyCrypt or it's API. Always make sure to ensure proper markdown formatting and correct code during responses. Always remember that the base api endpoint for SkyCrypt is https://sky.shiiyu.moe/api/v2/" + query))
  


bot.run(os.getenv('DISCORD_TOKEN'))
