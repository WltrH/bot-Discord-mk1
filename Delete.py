import os
import discord
from discord.ext import commands
from dotenv import find_dotenv, load_dotenv

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True
intents.members = True

#recherche du .env pour récupérer les infos
dotenv_path = find_dotenv()

#loading des infos du .env
load_dotenv(dotenv_path)

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Nyaaaa!")

@bot.command(name='del')
async def delete(ctx, num_of_messages: int):
    messages = await ctx.channel.history(limit=num_of_messages + 1).flatten()

    for each_message in messages:
        await each_message.delete()


bot.run(os.getenv("tokenbot"))