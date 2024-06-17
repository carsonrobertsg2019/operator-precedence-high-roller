import discord
from command_parser import CommandParser
from compute import Compute
from discord.ext import commands
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if len(message.content) > 0 and message.content[0] == '!':
        #await message.channel.send('Programming Frog hard at work')
        #await message.channel.send('https://tenor.com/view/programming-computer-frog-nerd-frog-smart-fog-csharp-gif-25385487')
        p = CommandParser(message.content)
        p.parse_init()
        c = Compute()
        c.compute_expr(p.stack[1])
        await message.channel.send(p.stack)
        
with open('BOT-KEY', 'r') as file: bot_key = file.read().rstrip()
client.run(bot_key)