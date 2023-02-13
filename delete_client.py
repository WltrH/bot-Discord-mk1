import discord



intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True
intents.members = True


client = discord.Client(intents = intents)

#Vérivication que le bot est bien lancé
@client.event
async def on_ready():
    print("Neko Ready for Duty!")

#réaction à un mot dans les messages
@client.event
async def on_message(message):
    text= message.content
    print(text)
    if message.content.lower() == "ping":
        await message.channel.send("pong")

#Message de bienvenue dans le channel général
@client.event
async def on_member_join(member):
    gen_channel = client.get_channel(1073345826102980800)
    await gen_channel.send(content=f"Bienvenue sur le Discord {member.display_name} !")




client.run(cf.tokenbot)