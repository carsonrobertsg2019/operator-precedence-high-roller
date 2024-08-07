import discord
from parsing.command_parser import CommandParser
from computing.compute import Compute
from json_handling import JsonHandling
from discord.ext import commands
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    json_handler = JsonHandling()
    c = Compute()
    if message.content.lower() == '!gamble' and not json_handler.gambling():
        await message.channel.send('odds or evens?')
        json_handler.update_json(gambling=True)
    elif json_handler.gambling() and 'odds or evens?' not in message.content.lower():
        if message.content.lower() == 'evens':
            json_handler.update_json(even=True)
        else:
            json_handler.update_json(even=False)
        json_handler.update_json(gambling=False)
        res = c.roll_die('d20')
        if int(res[0]) % 2 == 0:
            if json_handler.iseven():
                await message.channel.send(str(res[0]) + ' :slight_smile:')
            else:
                await message.channel.send(str(res[0]) + ' :slight_frown:')
        else:
            if json_handler.iseven():
                await message.channel.send(str(res[0]) + ' :slight_frown:')
            else:
                await message.channel.send(str(res[0]) + ' :slight_smile:')
    elif len(message.content) > 0 and message.content[0] == '!':
        json_handler.update_json(gambling=False)
        p = CommandParser(message.content)
        p.parse_init()
        if len(p.stack) < 2 or p.syntax_error:
            await message.channel.send('https://tenor.com/view/blm-gif-25815938')
        else:
            result = c.compute_expr(p.stack[1])
            if c.error:
                await message.channel.send('https://tenor.com/view/blm-gif-25815938')
            else:
                to_send = ""
                i = 0
                for cock in c.cocked_rolls:
                    to_send += "Honor the cock. Roll " + str(c.cocked_rolls[i][1]) + " was cocked. It would have been " + str(c.cocked_rolls[i][0]) + "\n"
                to_send += str(result[0]) + '\nDetails: ' + str(c.all_lists_of_rolls) + "\nAverage: " + str(result[1])
                if (len(to_send)) > 2000:
                    to_send_list = [(to_send[i:i+2000]) for i in range(0, len(to_send), 2000)]
                    for to_send in to_send_list:
                        await message.channel.send(to_send)
                else:
                    await message.channel.send(to_send)
    else:
        json_handler.update_json(gambling=False)
        
with open('BOT-KEY', 'r') as file: bot_key = file.read().rstrip()
client.run(bot_key)