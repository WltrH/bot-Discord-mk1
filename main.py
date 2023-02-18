import asyncio
import logging
import logging.handlers
import os
import dotenv
import youtube_dl
import botCommands
import voice

from typing import List, Optional

#import asyncpg  # asyncpg is not a dependency of the discord.py, and is only included here for illustrative purposes.
import discord
from discord.ext import commands
from aiohttp import ClientSession
from dotenv import find_dotenv, load_dotenv


#création de la class bot
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.typing = True
        intents.presences = True
        intents.message_content = True
        intents.members = True

        #recherche du .env pour récupérer les infos
        dotenv_path = find_dotenv()
        #loading des infos du .env
        load_dotenv(dotenv_path)

        super().__init__(command_prefix="/", intents=intents)
    #lancement du bot
    async def on_ready(self):
        print("Bot ready for duty!")



#classe pour les commandes de modération
class Moderation(commands.Cog):
    #funtion pour répondre pong
    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send("pong") 



#fonction main pour lancer le bot
async def main():
    async with bot:
        await bot.add_cog(Moderation(bot))
        await bot.start(os.getenv("tokenbot"))
        await bot.wait_until_ready()
        await bot.add_cog(botCommands.Music(bot))

#lancement du bot avec le token
if __name__ == "__main__":
    bot = Bot()
    asyncio.run(main())



    