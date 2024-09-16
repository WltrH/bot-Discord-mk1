#bibliothèque pour le bot
from aiohttp import ClientSession
import discord
from discord.ext import commands
import os
import youtube_dl
import asyncio

#-----------------commande pour mettre de la musique avec le bot-----------------

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
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
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #fonction pour joindre le channel vocal
    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        if ctx.voice_client is None:
            return await ctx.send("Le bot n'est pas présent dans le channel vocal")
        
        async with ctx.typing():
            try:
                source = await YTDLSource.from_url(query, loop=self.bot.loop)
                ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
                await ctx.send(f"**Le bot joue maintenant:** {source.title}")
            except Exception as e:
                await ctx.send(f"Une erreur s'est produite: {str(e)}")
    
    @commands.command()
    async def yt(self, ctx, *, url):
        await self.play(ctx, query=url)

    @commands.command()
    async def stream(self, ctx, *, url):
        if ctx.voice_client is None:
            return await ctx.send("Le bot n'est pas présent dans le channel vocal")
        
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('**Now playing:** {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Le bot n'est pas présent dans le channel vocal")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Le volume a été mis à {}%".format(volume))
    
    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("Le bot n'est pas présent dans le channel vocal")

        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("La musique a été mise en pause")
        else:
            await ctx.send("Aucune musique n'est en cours de lecture")
    
    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("Le bot n'est pas présent dans le channel vocal")

        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("La lecture a repris")
        else:
            await ctx.send("La musique n'est pas en pause")
    
    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("Le bot n'est pas présent dans le channel vocal")

        ctx.voice_client.stop()
        await ctx.send("La musique a été stoppée")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix='/', 
    description="Bot de musique",
    intents=intents,
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.start(os.environ["tokenbot"])

asyncio.run(main())
