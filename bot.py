import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#Initialize the database
data_path = r"data_file"
chroma_path = r"chroma_db"
chroma_client = chromadb.PersistentClient(path=chroma_path)
collection = chroma_client.get_or_create_collection(name="nike_pdf")

#Initialize the bot
intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents)

client = OpenAI()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')

@bot.command()
async def question(ctx, *, user_query: str):
    results = collection.query(query_texts=[user_query], n_results=1)

    #Handle no relevant documents
    if not results['documents'] or len(results['documents'][0]) == 0:
        await ctx.send("No relevant documents found. Please check the data.")
        return

    # Generate the OpenAI system prompt
    system_prompt = f"""
    You are a helpful assistant. You answer questions about the Nike annual report. But you only answer
    based on the knowledge I'm providing you. Don't use your internal knowledge and don't make anything up.
    If you don't know the answer, just reply with: I don't have the answer to this question, please ask a member of MDL.

    ---------------------

    The data:
        {str(results['documents'])}
    """

    response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_query}
    ]
    )

    reply = response.choices[0].message.content
    await ctx.send(reply[:2000])

bot.run(TOKEN)