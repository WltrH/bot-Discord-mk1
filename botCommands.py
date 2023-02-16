import os
import discord
from discord.ext import commands
import asyncio
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
    print("Bot ready for duty!")

# commande pour mettre en off le bot
@bot.command(name='off')
async def off(ctx):
    await ctx.send("Bot is off")
    await bot.close()

# commande ping pour vérifier que le bot est bien lancé
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send("pong")

# commande pour récupérer les information d'un utilisateur et les afficher dans le channel à son arrivée automatiquement
@bot.event
async def on_member_join(member):
    gen_channel = bot.get_channel(os.getenv("generalSalon"))
    await gen_channel.send(content=f"Bienvenue sur le Discord {member.display_name} !")

# commande pour récupérer des informations sur un autre discord en autorisant l'envoi de message dans le channel automatiquement dans le channel général
@bot.command(name='invite')
async def invite(ctx, url):
    await ctx.send(f"Invitation à rejoindre le discord {url}")
    gen_channel = bot.get_channel(os.getenv("generalSalon"))
    await gen_channel.send(content=f"Invitation à rejoindre le discord {url}")


# commande pour mute l'utilisateur pendant 10 minutes qui envoie un message avec un mot clé
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "discord.gg" in message.content:
        await message.delete()
        await message.author.edit(mute=True)
        await asyncio.sleep(600)
        print("Tu prends 600 secondes de mute, attention à tes paroles !")
    await bot.process_commands(message)


# commande pour faire venir le bot dans un salon vocal
@bot.command(name='come')
async def come(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

#coix du lien youtube à lire dans le salon vocal
@bot.command(name='play')
async def play(ctx, url):
    #si le bot n'est pas dans un salon vocal, il en rejoint le même que l'utilisateur
    if not ctx.guild.voice_client:
        await ctx.author.voice.channel.connect()
    #une fois le bot dans le salon vocal, il lit le lien youtube
        voice_client = ctx.guild.voice_client
        voice_client.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=url))

    
# commande pour récupérer le prix du bitcoin

bot.run(os.getenv("tokenbot"))