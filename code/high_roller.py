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
        p = CommandParser(message.content)
        p.parse_init()
        c = Compute()
        if len(p.stack) < 2 or p.syntax_error or c.error:
            await message.channel.send('https://tenor.com/view/blm-gif-25815938')    
        else:
            result = c.compute_expr(p.stack[1])
            to_send = ""
            i = 0
            for cock in c.cocked_rolls:
                to_send += "Honor the cock. Roll " + str(c.cocked_rolls[i][1]) + " was cocked. It would have been " + str(c.cocked_rolls[i][0]) + "\n"
            to_send += str(result) + '\nDetails: ' + str(c.all_lists_of_rolls)
            if (len(to_send)) > 2000:
                to_send_list = [(to_send[i:i+2000]) for i in range(0, len(to_send), 2000)]
                for to_send in to_send_list:
                    await message.channel.send(to_send)
            else:
                await message.channel.send(to_send)            
        
with open('BOT-KEY', 'r') as file: bot_key = file.read().rstrip()
client.run(bot_key)