import discord
from discord.ext import commands
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if len(message.content) > 0 and message.content[0] == '!':
        await message.channel.send(message.content)
            
with open('BOT-KEY', 'r') as file: bot_key = file.read().rstrip()
client.run(bot_key)