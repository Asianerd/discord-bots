import math
import discord
import json
from enum import Enum

import Formatting
from Game import StatusEffects
from Game.StatusEffects import EffectContainer
from Game import GameValue


class BattleProfile:
    collection = []

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

        self.health = GameValue.GameValue(0, 100, 1)

        self.effects = EffectContainer()

        self.current_weapon = None

        self.enemies = []

        self.battle_results = [0, 0]  # 0:wins  1:losses

    async def display_stats(self, ctx):
        color = Formatting.dynamic_color(1-self.health.percent())
        await ctx.send(embed=discord.Embed(
            title=f"{self.name}",
            description=f"Health : {self.health.current}/{self.health.max} : {int(self.health.percent() * 100)}%",
            colour=int((int(color[0])) + (int(color[1]) * 256))
        ))

    def as_dict(self):
        final = dict(self.__dict__)
        final['health'] = self.health.as_dict()
        final['effects'] = self.effects.as_dict()
        return final

    def load_from_dict(self, data_dict):
        self.__dict__ = dict(data_dict)
        self.health = GameValue.GameValue.object_from_dict(self.health)
        self.effects = EffectContainer.object_from_dict(self.effects)

    @staticmethod
    def save():
        final = {}
        for x in BattleProfile.collection:
            final[str(x.user_id)] = x.as_dict()
        with open('Data/battle_profiles.json', 'w', encoding='utf-8') as file:
            json.dump(final, file, indent=4)

    @staticmethod
    def load():
        BattleProfile.collection = []
        with open('Data/battle_profiles.json', 'r', encoding='utf-8') as file:
            data_file = json.load(file)
            for x in data_file.items():
                data = x[1]

                item = BattleProfile('', 0)
                item.load_from_dict(data)
                BattleProfile.collection.append(item)

    @staticmethod
    def update_user(username, user_id):
        if len([x for x in BattleProfile.collection if x.user_id == user_id]) == 0:
            BattleProfile.collection.append(BattleProfile(username, user_id))

        [x for x in BattleProfile.collection if x.user_id == user_id][0].name = username

        BattleProfile.save()

    @staticmethod
    def fetch_user(user_id):
        return [x for x in BattleProfile.collection if x.user_id == user_id][0]


class Enemy:
    enemy_stats = {}

    @staticmethod
    def initialize():
        with open('enemy_stats.json', 'r', encoding='utf-8') as file:
            Enemy.enemy_stats = json.load(file)

    def __init__(self, species):
        data_table = Enemy.enemy_stats[species.name]
        self.species = species
        self.name = data_table['name']
        self.health = GameValue(
            data_table['health']['min'],
            data_table['health']['max'],
            data_table['health']['regen'],
            data_table['health']['starting_percent'],
        )

        # basic 'damage every round' for now
        self.damage = data_table['damage']

    def is_dead(self):
        return self.health.percent() <= 0

    class Species(Enum):
        zombie = 0
        undead_miner = 1
        goblin = 2
