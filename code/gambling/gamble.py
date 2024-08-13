import discord
from parsing.command_parser import CommandParser
from computing.compute import Compute
from json_handling import JsonHandling
from discord.ext import commands

class Gamble:
    def __init__(self, message, c):
        self.message = message
        self.c = c
        self.json_handler = JsonHandling(playername=message.author.name)
        self.even = False

    def update_gambling_state(self, gambling_state):
        self.json_handler.update_json(self.message.author.name, gambling_state)

    def gambling(self):
        return self.json_handler.gambling(self.message.author.name)

    async def determine_call(self):
        if self.message.content.lower() == 'evens':
            self.even = True
            self.json_handler.update_json(self.message.author.name, False)
        elif self.message.content.lower() == 'odds':
            self.even = False
            self.json_handler.update_json(self.message.author.name, False)

    async def determine_result(self):
        res = self.c.roll_die('d20')
        if int(res[0]) % 2 == 0:
            if self.even:
                await self.message.channel.send(str(res[0]) + ' :money_mouth:')
            else:
                await self.message.channel.send(str(res[0]) + ' :japanese_ogre:')
        else:
            if self.even:
                await self.message.channel.send(str(res[0]) + ' :japanese_ogre:')
            else:
                await self.message.channel.send(str(res[0]) + ' :money_mouth:')
