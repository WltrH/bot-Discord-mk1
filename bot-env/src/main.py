import discord
import config as cf
intents = discord.Intents.default()
intents.typing = False
intents.presences = False


client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print("Nyaaaa!")

@client.event
async def on_message(message):
    print(message.content)


client.run(cf.tokenbot)