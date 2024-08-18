from json_handling.json_handle import JsonHandle
from datetime import datetime
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import time

class RollPersistence:
    def __init__(self, message, c):
        self.message = message
        self.c = c
        self.json_handler = JsonHandle(playername=message.author.name)

    def add_rolls_to_json(self):
        i = 0
        for list_of_rolls in self.c.all_lists_of_rolls:
            for roll in list_of_rolls:
                self.json_handler.add_roll(
                    self.message.author.name,
                    self.c.list_of_dice[i],
                    roll,
                    datetime.timestamp(datetime.now())
                )
                i += 1

    def get_rolls_from_json(self, seconds_to_subtract=43200, die_to_show="d20"):
        rolls = self.json_handler.get_rolls(self.message.author.name)
        recent_rolls = []
        for i in range(len(rolls)):
            ts = rolls[i]["timestamp"]
            die = rolls[i]["die"]
            if ts > time.time() - seconds_to_subtract and die == die_to_show:
                recent_rolls.append(rolls[i])
        results = [0]*20
        for i in range(len(recent_rolls)):
            results[recent_rolls[i]["roll"]-1] += 1
        ax = sns.barplot(x=np.arange(1,21), y=results)
        ax.bar_label(ax.containers[0])
        plt.axis('off')
        plt.savefig('bar_plots/bar_plot_' + self.message.author.name + '.png')
        plt.clf()