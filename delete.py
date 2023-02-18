import discord
import os

from dotenv import load_dotenv

load_dotenv()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


    async def on_message(self, message):
        if message.content.startswith('/delete'):
            msg = await message.channel.send('Deleting messages...')
            await msg.delete()

    async def on_message_delete(self, message):
        msg = f'{message.author} deleted the message: {message.content}'
        await message.channel.send(msg)


intents = discord.Intents.default()
intents.message = True

client = MyClient(intents=intents)
client.run(os.environ["tokenbot"])