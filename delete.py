import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class MyClient(commands.Bot):
    async def on_ready(self):
        print(f'Connecté en tant que {self.user} (ID: {self.user.id})')
        print('------')

    @commands.command(name='delete')
    async def delete_messages(self, ctx, amount: int):
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        msg = await ctx.send(f'{len(deleted)} messages supprimés.')
        await msg.delete(delay=5)

    async def on_message_delete(self, message):
        if message.author.bot:
            return
        msg = f'{message.author} a supprimé le message : {message.content}'
        await message.channel.send(msg)

intents = discord.Intents.default()
intents.message_content = True

bot = MyClient(command_prefix='/', intents=intents)
bot.run(os.getenv("tokenbot"))