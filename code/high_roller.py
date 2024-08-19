import discord
from parsing.command_parser import CommandParser
from computing.compute import Compute
from json_handling.json_handle import JsonHandle
from json_handling.gamble.gamble import Gamble
from json_handling.roll_persistence.roll_persistence import RollPersistence
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

def channel_valid(message):
    keywords = [
        'dnd',
        "dice",
        "rolls",
        "dumpster",
        "box-of-doom",
        "gamblers"
    ]
    valid = False
    for word in keywords:
        if word in message.channel.name: valid = True
    return valid

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    c = Compute()
    jh = JsonHandle(message.author.name)
    gamble = Gamble(message, c)
    rp = RollPersistence(message, c)
    g = gamble.gambling()
    if not channel_valid(message) and (message.content[0] == '!' or message.content in ['odds', 'evens']):
        await message.channel.send("https://tenor.com/view/blm-gif-25815938")
    elif message.content.lower() == '!gamble' and not gamble.gambling():
        await message.channel.send('odds or evens?')
        gamble.update_gambling_state(True)
    elif gamble.gambling() and message.author.name != 'High Roller':
        await gamble.determine_call()
        if not gamble.gambling():
            await gamble.determine_result()
    elif '!c' in message.content.lower() and message.content[0] == '!':
        jh.clear_player_data()
    elif '!h' == message.content.lower() and message.content[0] == '!':
        rp.get_rolls_from_json()
        await message.channel.send(file=discord.File('bar_plots/bar_plot_' + message.author.name + '.png'))
    elif len(message.content) > 0 and message.content[0] == '!':
        p = CommandParser(message.content)
        p.parse_init()
        if len(p.stack) < 2 or p.syntax_error:
            await message.channel.send('https://tenor.com/view/blm-gif-25815938')
        else:
            result = c.compute_expr(p.stack[1])
            if c.error:
                await message.channel.send('https://tenor.com/view/blm-gif-25815938')
            else:
                rp.add_rolls_to_json()
                to_send = ""
                i = 0
                for cock in c.cocked_rolls:
                    to_send += "Honor the cock. Roll " + str(c.cocked_rolls[i][1]) + " was cocked. It would have been " + str(c.cocked_rolls[i][0]) + "\n"
                    i += 1
                to_send += str(result[0]) + '\nDetails: ' + str(c.all_lists_of_rolls) + "\nAverage: " + str(result[1])
                if (len(to_send)) > 2000:
                    to_send_list = [(to_send[i:i+2000]) for i in range(0, len(to_send), 2000)]
                    for to_send in to_send_list:
                        await message.channel.send(to_send)
                else:
                    await message.channel.send(to_send)
        
with open('BOT-KEY', 'r') as file: bot_key = file.read().rstrip()
client.run(bot_key)