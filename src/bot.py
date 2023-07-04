import os
import nextcord
import requests
import json
import re
import sys
from nextcord.ext import commands
from dotenv import load_dotenv
from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI


load_dotenv()

bot = commands.Bot()
TESTING_GUILD_ID = 1125840466366189598
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_KEY')

def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return index

def query(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response


@bot.event
async def on_ready():
    print(f'Login as {bot.user} successful!')

@bot.slash_command(description="Queries the SkyCrypt Knowledgebase!", guild_ids=[TESTING_GUILD_ID])
async def sky(interaction: nextcord.Interaction,query: str):
    await interaction.response.send_message(query(query))

index = construct_index("src\docs") #Hard Coded for now :)

bot.run(os.getenv('DISCORD_TOKEN'))