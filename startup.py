import asyncio
import logging
import logging.handlers
import os
import dotenv
import youtube_dl

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

        super().__init__(command_prefix="!", intents=intents)
    #lancement du bot
    async def on_ready(self):
        print("Bot ready for duty!")



#classe pour les commandes de modération
class Moderation(commands.Cog):
    #funtion pour répondre pong
    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send("pong") 


#-----------------commande pour mettre de la musique avec le bot-----------------

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

    #fonction pour joindre le channel vocal
    @commands.command(name='join', help='Tells the bot to join the voice channel')
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} n'est pas présent dans le channel vocal".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("Le bot vous a rejoins dans le channel vocal.")
    
    #fonction pour jouer de la musique
    @commands.command(name='play', help='To play music')
    async def play(ctx, url):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client

            async with ClientSession() as session:
                player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
                voice_channel.play(discord.FFmpegPCMAudio(player, **ffmpeg_options))

                await ctx.send('**Joue maintenant:** {}'.format(player.title))
        except:
            await ctx.send("Le bot n'est pas présent dans le channel vocal")

    #fonction pour mettre en pause la musique
    @commands.command(name='pause', help='This command pauses the song')
    async def pause(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("La musique n'est pas en cours de lecture.")
    #fonction pour reprendre la musique
    @commands.command(name='resume', help='This command resumes the song')
    async def resume(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
        else:
            await ctx.send("La musique n'est pas en pause.")

    #fonction pour stopper la musique
    @commands.command(name='stop', help='This command stops the song')
    async def stop(ctx):
        voice_client = ctx.message.guild.voice_client
        voice_client.stop()
        



#fonction main pour lancer le bot
async def main():
    async with bot:
        await bot.add_cog(Moderation(bot))
        await bot.start(os.getenv("tokenbot"))

#lancement du bot avec le token
if __name__ == "__main__":
    bot = Bot()
    asyncio.run(main())