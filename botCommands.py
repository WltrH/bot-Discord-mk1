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


bot.run(os.getenv("tokenbot"))