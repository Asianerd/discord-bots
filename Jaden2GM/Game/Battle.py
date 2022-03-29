import math
import discord
from discord.ext import commands
import json
from enum import Enum

import Formatting
import Dependencies

from User import User

from Game import StatusEffects
from Game.StatusEffects import EffectContainer
from Game import GameValue
from Game import ItemClass
from Game.ItemClass import ItemType, Equipment, Consumable


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
        final = discord.Embed(
            title=f"{self.name}",
            description=
            f"**Health** : `{self.health.current}/{self.health.max}` ({int(self.health.percent() * 100)}%)" + (
                '\n' + '**Effects** : ' + ' ,'.join([f'{EffectContainer.display_names[x[0]]}[{x[1]}]' for x in self.effects.effects.items()])
                if self.effects.effects else ''),
            colour=int((int(color[0]) * 65536) + (int(color[1]) * 256))
        )
        await ctx.send(embed=final)

    async def display_enemy_stats(self, ctx, send=True):
        final = discord.Embed(
            title="Enemies",
            colour=Dependencies.battle_embed_colour
        )

        """
        name
        health : i/max
        damage : ....
        effects : .........
        
        
        """

        for index, x in enumerate(self.enemies):
            if x.is_dead():
                final.add_field(
                    name=f'~~{index+1}. {x.name}~~',
                    value='_Dead_'
                )
            else:
                final.add_field(
                    name=f'{index+1}. {x.name}',
                    value=f'_Health_ : `{x.health.current}/{x.health.max}`\n'\
                          f'_Damage_ : `{x.damage}`\n' + (f'_Effects_ : ' + ', '.join([f'{EffectContainer.display_names[i[0]]}[{i[1]}]' for i in x.effects.items()]) if len(x.effects) else '')
                )

        if send:
            await ctx.send(embed=final)
        else:
            return final

    def as_dict(self):
        final = dict(self.__dict__)
        final['health'] = self.health.as_dict()
        final['effects'] = self.effects.as_dict()
        final['enemies'] = [x.as_dict() for x in final['enemies']]
        return final

    def load_from_dict(self, data_dict):
        self.__dict__ = dict(data_dict)
        self.health = GameValue.GameValue.object_from_dict(self.health)
        self.effects = EffectContainer.object_from_dict(self.effects)
        self.enemies = [Enemy.object_from_dict(x) for x in data_dict['enemies']]

    def apply_effect(self, effect, duration):
        if effect in self.effects.effects:
            if duration > self.effects.effects[effect]:
                self.effects.effects[effect] = duration
        else:
            self.effects.effects[effect] = duration

    async def progress_game(self, ctx):
        if [x for x in self.enemies if not x.is_dead()]:
            # if there are enemies that are alive
            final_embed = await self.display_enemy_stats(ctx, send=False)
            final_embed.title = "Enemy's turn"
            final_embed.colour = Dependencies.battle_embed_colour

            final = ''
            final_damage = 0
            for enemy in self.enemies:
                if enemy.is_dead():
                    continue
                final_damage += enemy.damage
                final += f'_**{enemy.name}** attacked for `{enemy.damage}`_\n'
            final_embed.description = final + f'\n\n**Total damage taken :** `{final_damage}`'
            await ctx.send(embed=final_embed)

            self.health.current -= final_damage
            self.effects.update()

            await self.display_stats(ctx)

        else:
            if len(self.enemies) <= 0:
                await ctx.send(embed=discord.Embed(
                    title='No enemies to fight!',
                    colour=Dependencies.default_embed_colour
                ))
            else:
                coin_reward = sum([x.coin_reward for x in self.enemies])
                item_rewards = {
                    ItemType.consumable: {

                    },
                    ItemType.equipment: {

                    }
                }
                for x in self.enemies:
                    loot = x.fetch_rewards()
                    for item in loot[ItemType.consumable].items():
                        if not (item[0] in item_rewards[ItemType.consumable]):
                            item_rewards[ItemType.consumable][item[0]] = 0
                        item_rewards[ItemType.consumable][item[0]] += item[1]

                    for item in loot[ItemType.equipment].items():
                        if not (item[0] in item_rewards[ItemType.equipment]):
                            item_rewards[ItemType.equipment][item[0]] = 0
                        item_rewards[ItemType.equipment][item[0]] += item[1]
                reward_string = ''

                if len(item_rewards[ItemType.consumable]):
                    reward_string += '***Consumables***\n'
                for x in item_rewards[ItemType.consumable].items():
                    reward_string += f'{Consumable.item_symbols[x[0]]} **{Consumable.display_names[x[0]]} [{x[1]}]**\n'

                if len(item_rewards[ItemType.equipment]):
                    reward_string += '\n***Equipment***\n'
                for x in item_rewards[ItemType.equipment].items():
                    reward_string += f'{x[0].name}[{x[1]}]'

                user = User.fetch_user(self.user_id, self.name)
                for item_class in item_rewards.items():
                    for item in item_class[1].items():
                        user.append_inventory(item[0], item_class[0], item[1])

                await ctx.send(embed=discord.Embed(
                    title='You emerge victorious!',
                    description=f'Rewards :\n**{coin_reward} coins**\n\n' + reward_string,
                    colour=Dependencies.success_embed_colour
                ))

                self.enemies = []

                BattleProfile.save()

    async def attack(self, ctx, index):
        # TODO : make this the actual weapon damage
        damage = 10
        enemy = self.enemies[index]
        enemy.health.current -= damage
        await ctx.send(embed=discord.Embed(
            title=f"Attacked {enemy.name} for {damage} damage!",
            colour=Dependencies.success_embed_colour
        ))

    def apply_health(self, amount):
        if self.health.percent() <= 1:
            final_amount = amount
        else:
            if self.health.percent() > 2:
                self.health.current = self.max * 2
                final_amount = 0
            else:
                multiplier = 2 - self.health.percent()
                #self.health.current += int(amount * multiplier)
                final_amount = int(amount * multiplier)
        self.health.current += final_amount

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
        with open('Data/enemy_stats.json', 'r', encoding='utf-8') as file:
            Enemy.enemy_stats = json.load(file)

    def __init__(self, species):
        data_table = Enemy.enemy_stats[species.name]
        self.species = species
        self.name = data_table['name']
        self.health = GameValue.GameValue(
            data_table['health']['min'],
            data_table['health']['max'],
            data_table['health']['regen'],
            data_table['health']['starting_percent'],
        )

        # basic 'damage every round' for now
        self.damage = data_table['damage']
        self.defense = data_table['defense']

        self.effects = {}

        self.loot_table = {
            ItemType.equipment:{

            },
            ItemType.consumable:{

            }
        }
        self.coin_reward = data_table['coin_reward']
        self.get_loot_table(data_table['loot_table'])

    def get_loot_table(self, data_table):
        # called when new Enemy is created
        # loot table is not saved, a new one is created on startup
        for item in data_table['equipment'].items():
            self.loot_table[ItemType.equipment][Equipment.get_enum(item[0])] = item[1]

        for item in data_table['consumable'].items():
            self.loot_table[ItemType.consumable][Consumable.get_enum(item[0])] = item[1]

    def is_dead(self):
        return self.health.percent() <= 0

    def fetch_rewards(self):
        return dict(self.loot_table)

    @staticmethod
    def object_from_dict(data_dict):
        final = Enemy(Enemy.get_enum(data_dict['species']))
        final.health = GameValue.GameValue.object_from_dict(data_dict['health'])
        _effects = {}
        for x in data_dict['effects'].items():
            _effects[StatusEffects.get_enum(x[0])] = x[1]
        final.effects = dict(_effects)
        return final

    def as_dict(self):
        final = dict(self.__dict__)
        final['species'] = final['species'].name

        final['health'] = self.health.as_dict()
        _effects = {}
        for x in self.effects.items():
            _effects[x[0].name] = x[1]
        final['effects'] = _effects

        final.pop('loot_table')
        return final

    @staticmethod
    def get_enum(name):
        for x in Enemy.Species:
            if x.name == name:
                return x

    class Species(Enum):
        zombie = 0
        undead_miner = 1
        goblin = 2
