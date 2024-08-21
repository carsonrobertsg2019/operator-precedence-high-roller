import discord
from parsing.command_parser import CommandParser
from parsing.enums.command_type import CommandType
from computing.compute import Compute
from json_handling.gamble.gamble import Gamble
from json_handling.roll_persistence.roll_persistence import RollPersistence
import message_validator as mv
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if not mv.channel_valid(message) and mv.message_is_command(message):
        await message.channel.send("https://tenor.com/view/blm-gif-25815938")
    elif mv.message_is_command(message):
        compute = Compute()
        gamble = Gamble(message, compute)
        rollPersistence = RollPersistence(message, compute)
        commandParser = CommandParser(message.content)
        commandParser.parse_init()
        if commandParser.command_type == CommandType.ERROR:
            await message.channel.send("https://tenor.com/view/blm-gif-25815938")
        elif commandParser.command_type == CommandType.GAMBLE_START:
            if not gamble.gambling():
                await message.channel.send('odds or evens?')
                gamble.update_gambling_state(True)
        elif commandParser.command_type == CommandType.GAMBLE_BET:
            if await gamble.determine_bet(commandParser.stack[1].token_info.lexeme):
                if gamble.gambling():
                    await gamble.determine_result()
                    gamble.update_gambling_state(False)
        elif commandParser.command_type == CommandType.RECALL_ROLLS:
            if len(commandParser.stack) == 2:
                rollPersistence.get_rolls_from_json()
            elif len(commandParser.stack) == 7:
                rollPersistence.get_rolls_from_json(
                    int(commandParser.stack[3].token_info.lexeme), 
                    commandParser.stack[5].token_info.lexeme
                )
            await message.channel.send(file=discord.File('bar_plots/bar_plot_' + message.author.name + '.png'))
        elif commandParser.command_type == CommandType.EXPR:
            result = compute.compute_expr(commandParser.stack[1])
            if compute.error:
                await message.channel.send('https://tenor.com/view/blm-gif-25815938')
            else:
                rollPersistence.add_rolls_to_json()
                to_send = ""
                i = 0
                for cock in compute.cocked_rolls:
                    to_send += "Honor the cock. Roll " + str(compute.cocked_rolls[i][1]) + " was cocked. It would have been " + str(compute.cocked_rolls[i][0]) + "\n"
                    i += 1
                to_send += str(result[0]) + '\nDetails: ' + str(compute.all_lists_of_rolls) + "\nAverage: " + str(result[1])
                if (len(to_send)) > 2000:
                    to_send_list = [(to_send[i:i+2000]) for i in range(0, len(to_send), 2000)]
                    for to_send in to_send_list:
                        await message.channel.send(to_send)
                else:
                    await message.channel.send(to_send)
with open('BOT-KEY', 'r') as file: bot_key = file.read().rstrip()
client.run(bot_key)