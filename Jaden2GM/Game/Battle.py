import math
import discord
from discord.ext import commands
import json
from enum import Enum
from collections import Counter

import Formatting
import Dependencies

from User import User

from Game import StatusEffects
from Game.StatusEffects import EffectContainer
from Game import GameValue
from Game import ItemClass
from Game.ItemClass import ItemType, Consumable, Weapon, Blessing

# real funny python


battle_reactions = {
    "dodge": "💨",
    "numbers": [
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣",
        "🔟"
    ]
}


class BattleProfile:
    collection = []
    client: commands.Bot = None

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

        self.coins = 0

        self.level = 0
        self.level_value = GameValue.GameValue(0, 100, 0)

        self.health = GameValue.GameValue(0, 100, 1)
        self.mana = GameValue.GameValue(0, 100, 3)
        self.stamina = GameValue.GameValue(0, 100, 3)

        self.defense = 0
        self.dodge_chance = 5
        self.crit_chance = 10

        self.effects = EffectContainer()

        self.current_weapon: Weapon = None

        self.enemies = []

        self.backpack = {}  # For consumables
        self.weapons = {}
        self.blessings = {}

        self.equipped_blessings = {

        }
        self.quickslot = []

        self.battle_results = [0, 0]  # 0:wins  1:losses

        self.enemy_message = 0
        self.player_message = 0

        """
        player stats
        
        HP
        X ATK
        defense
        dodge chance
        Mana
        Stamina
        """

    # region Displays
    def update_stats(self, regen=True):
        self.effects.calculate_combination(self)

        container = self.effects.property_container
        self.health.max = 100 * container.max_health
        self.stamina.max = 100 * container.max_stamina
        self.mana.max = 100 * container.max_mana

        self.health.regeneration = int(1 * container.health_regen)
        self.stamina.regeneration = int(3 * container.stamina_regen)
        self.mana.regeneration = int(3 * container.mana_regen)

        self.defense = 0 * container.defense
        self.crit_chance = 10 * container.crit_chance
        self.dodge_chance = 5 * container.dodge_chance

        if regen:
            self.regenerate()
            self.effects.update()

    async def update_displays(self, ctx: discord.abc.Messageable, enemy_embed, player_embed):
        try:
            enemy_message = await ctx.fetch_message(self.enemy_message)
            player_message = await ctx.fetch_message(self.player_message)
            await enemy_message.edit(embed=enemy_embed)
            await player_message.edit(embed=player_embed)
        except Exception as e:
            enemy_message = await ctx.send(embed=enemy_embed)
            player_message = await ctx.send(embed=player_embed)
            self.enemy_message = enemy_message.id
            self.player_message = player_message.id
        enemy_indexes = [i for i, x in enumerate(self.enemies) if not x.is_dead()]
        to_be_added = [battle_reactions['numbers'][x] for x in enemy_indexes]
        to_be_added.insert(0, battle_reactions['dodge'])
        for x in enemy_message.reactions:
            if x.emoji not in to_be_added:
                await enemy_message.clear_reaction(x.emoji)
        for x in to_be_added:
            if x in [i.emoji for i in enemy_message.reactions]:
                continue
            await enemy_message.add_reaction(x)

    async def display_stats(self, ctx, send=True):
        color = Formatting.dynamic_color(1 - self.health.percent())
        self.update_stats(regen=False)
        # :hearts: :four_leaf_clover: :zap:
        final = discord.Embed(
            title=f"{self.name}",
            description=f":hearts: : {Formatting.progress_bar(self.health.percent(), 'h')} {' +'[self.health.percent() > 1]} `{int(self.health.current)}/{int(self.health.max)}` `+{self.health.regeneration}`\n"
                        f":zap: : {Formatting.progress_bar(self.stamina.percent(), 's')} {' +'[self.stamina.percent() > 1]} `{int(self.stamina.current)}/{int(self.stamina.max)}` `+{self.stamina.regeneration}`\n"
                        f":four_leaf_clover: : {Formatting.progress_bar(self.mana.percent(), 'm')} {' +'[self.mana.percent() > 1]} `{int(self.mana.current)}/{int(self.mana.max)}` `+{self.mana.regeneration}`\n"
                        f":dagger: `{round((self.current_weapon.damage if self.current_weapon else 5) * self.effects.property_container.damage, 2)}` :shield: : `{int(self.defense)}` :dash: : `{round(self.dodge_chance, 3)}%`\n",
            colour=int((int(color[0]) * 65536) + (int(color[1]) * 256))
        )
        if self.current_weapon:
            final.description = f"**Weapon** : _{ItemClass.equipment_stats['item_symbols'][self.current_weapon.weapon_type.name]} {self.current_weapon.name}_\n" + final.description
        else:
            final.description = f"**Weapon** : _None_\n\n" + final.description
        if len(self.effects.effects):
            final.add_field(name='**Effects**', value=' ,'.join(
                [f'{EffectContainer.display_names[x[0]]}[{x[1]}]' for x in self.effects.effects.items()]))
        if send:
            await ctx.send(embed=final)
        else:
            return final

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
                    name=f'~~{index + 1}. {x.name}~~',
                    value='_Dead_'
                )
            else:
                final.add_field(
                    name=f'{index + 1}. {x.name}',
                    value=f'_Health_ : `{x.health.current}/{x.health.max}`\n'
                          f'_Damage_ : `{x.damage}`\n' + (f'_Effects_ : ' + ', '.join(
                        [f'{EffectContainer.display_names[i[0]]}[{i[1]}]' for i in x.effects.items()]) if len(
                        x.effects) else '')
                )

        if send:
            await ctx.send(embed=final)
        else:
            return final
    # endregion

    # region Data-related
    def as_dict(self):
        final = dict(self.__dict__)
        final['level_value'] = self.level_value.as_dict()

        final['health'] = self.health.as_dict()
        final['mana'] = self.mana.as_dict()
        final['stamina'] = self.stamina.as_dict()

        if self.current_weapon:
            final['current_weapon'] = self.current_weapon.item_id.name

        final['effects'] = self.effects.as_dict()
        final['enemies'] = [x.as_dict() for x in final['enemies']]

        final['backpack'] = dict([(x[0].name, x[1]) for x in self.backpack.items()])
        final['weapons'] = dict([(x[0].name, x[1]) for x in self.weapons.items()])
        final['blessings'] = dict([(x[0].name, x[1]) for x in self.blessings.items()])

        final['equipped_blessings'] = dict([(x[0].name, x[1].as_dict()) for x in self.equipped_blessings.items()])
        final['quickslot'] = [x.as_dict() for x in self.quickslot]

        final['enemy_message'] = 0
        final['player_message'] = 0

        return final

    def load_from_dict(self, data_dict):
        self.__dict__ = dict(data_dict)

        self.level_value = GameValue.GameValue.object_from_dict(self.level_value)

        self.health = GameValue.GameValue.object_from_dict(self.health)
        self.mana = GameValue.GameValue.object_from_dict(self.mana)
        self.stamina = GameValue.GameValue.object_from_dict(self.stamina)

        if self.current_weapon:
            self.current_weapon = ItemClass.Weapon(ItemClass.Weapon.get_enum(self.current_weapon))

        self.effects = EffectContainer.object_from_dict(self.effects)
        self.enemies = [Enemy.object_from_dict(x) for x in data_dict['enemies']]

        self.backpack = dict([(Consumable.get_enum(x[0]), x[1]) for x in data_dict['backpack'].items()])
        self.weapons = dict([(Weapon.get_enum(x[0]), x[1]) for x in data_dict['weapons'].items()])
        self.blessings = dict([(Blessing.get_enum(x[0]), x[1]) for x in data_dict['blessings'].items()])

        self.equipped_blessings = dict(
            [(
                [i for i in Blessing.BlessingType if i.name.lower() == x[0].lower()],
                Blessing.object_from_dict(x[1])
            ) for x in data_dict['equipped_blessings']])
        self.quickslot = [Weapon.object_from_dict(x) for x in data_dict['quickslot']]

        self.enemy_message = 0
        self.player_message = 0
    # endregion

    # region Game-related
    def apply_effect(self, effect, duration):
        if effect in self.effects.effects:
            if duration > self.effects.effects[effect]:
                self.effects.effects[effect] = duration
        else:
            self.effects.effects[effect] = duration

    async def progress_game(self, ctx, action_type, enemy_index=0):
        if [x for x in self.enemies if not x.is_dead()]:
            # region Update/regen player stats
            self.update_stats()
            # endregion

            # region Embed stuff
            if action_type == BattleProfile.ActionType.dodge:
                self.dodge_chance = 90
                _t = "You tried dodging incoming attacks!"
            elif action_type == BattleProfile.ActionType.attack:
                _t = f"You attacked for {self.attack(enemy_index)} damage!"
            else:
                _t = "You didn't do anything!"

            final_embed = await self.display_enemy_stats(ctx, send=False)
            final_embed.title = _t
            final_embed.colour = Dependencies.battle_embed_colour
            # endregion

            # region Damage stuff
            final = ''
            final_damage = 0
            for enemy in self.enemies:
                if enemy.is_dead():
                    continue
                if not Dependencies.chance(self.dodge_chance):
                    final_damage += enemy.damage
                    final += f'**>** _**{enemy.name}** attacked for `{enemy.damage}`_\n'
                else:
                    final += f'**>** _**{enemy.name}** missed!_\n'

            # final_damage += int(final_damage - (final_damage * self.effects.property_container['defense']))
            final_damage -= int(self.defense * self.effects.property_container.defense)
            final_damage = 0 if final_damage < 0 else final_damage  # ensure positive damage
            self.health.current -= final_damage
            # endregion

            final += f"\n**{'▄' * 30}**\n"
            final_embed.description = final

            await self.update_displays(ctx, final_embed, await self.display_stats(ctx, send=False))

        # condition is checked again, for when the round ends
        if [x for x in self.enemies if not x.is_dead()]:
            pass
        else:
            if len(self.enemies) <= 0:
                await ctx.send(embed=discord.Embed(
                    title='No enemies to fight!',
                    colour=Dependencies.default_embed_colour
                ))
            else:
                # region Loot stuff
                coin_reward = sum([x.coin_reward for x in self.enemies])
                item_rewards = {
                    ItemType.consumable: {},
                    ItemType.weapon: {},
                    ItemType.blessing: {}
                }
                for x in self.enemies:
                    loot = x.fetch_rewards()
                    for i in [
                        ItemType.consumable,
                        ItemType.weapon,
                        ItemType.blessing
                    ]:
                        for item in loot[i].items():
                            if not (item[0] in item_rewards[i]):
                                item_rewards[i][item[0]] = 0
                            item_rewards[i][item[0]] += item[1]

                reward_string = ''

                if len(item_rewards[ItemType.consumable]):
                    reward_string += '***Consumables***\n' + '\n'.join([f'** · ' + (f'[{x[1]}]' if x[1] > 1 else '') + f' {Consumable.item_symbols[x[0]]} {Consumable.display_names[x[0]]}**' for x in item_rewards[ItemType.consumable].items()])

                if len(item_rewards[ItemType.weapon]):
                    reward_string += '\n\n***Weapons***\n'
                    for x in item_rewards[ItemType.weapon].items():
                        w = ItemClass.equipment_stats[ItemType.weapon][x[0].name]
                        reward_string += "** · " + (f'[{x[1]}]' if x[1] > 1 else '') + f" {ItemClass.equipment_stats['item_symbols'][w['weapon_type']]} {w['name']}**\n"

                if len(item_rewards[ItemType.blessing]):
                    reward_string += '\n***Blessings***\n'
                    for x in item_rewards[ItemType.blessing].items():
                        b = ItemClass.equipment_stats[ItemType.blessing][x[0].name]
                        reward_string += "** · " + (f'[{x[1]}]' if x[1] > 1 else '') + f" {ItemClass.equipment_stats['item_symbols'][b['blessing_type']]} {b['name']}**\n"

                for item_type, container in [
                    [ItemType.consumable, self.backpack],
                    [ItemType.weapon, self.weapons],
                    [ItemType.blessing, self.blessings]
                ]:
                    for item in item_rewards[item_type].items():
                        if not (item[0] in container):
                            container[item[0]] = 0
                        container[item[0]] += item[1]
                # endregion

                exp_reward = sum([x.exp_reward for x in self.enemies])

                await ctx.send(embed=discord.Embed(
                    title='You emerge victorious!',
                    description=f'**Rewards** :\n**{coin_reward} coins**\n**{exp_reward} experience**\n\n' + reward_string,
                    colour=Dependencies.success_embed_colour
                ))

                await self.increase_level(ctx, exp_reward)
                self.coins += coin_reward

                self.enemies = []
                self.battle_results[0] += 1

                self.player_message = 0
                self.enemy_message = 0

                BattleProfile.save()

    def attack(self, index):
        if self.current_weapon:
            damage = self.current_weapon.damage
        else:
            damage = 5
        damage = int(damage * self.effects.property_container.damage)
        enemy = self.enemies[index]
        enemy.health.current -= damage

        return damage  # returns damage for embed use

    def apply_health(self, amount):
        if self.health.percent() <= 1:
            final_amount = amount
        else:
            if self.health.percent() > 2:
                self.health.current = self.health.max * 2
                final_amount = 0
            else:
                multiplier = 2 - self.health.percent()
                # self.health.current += int(amount * multiplier)
                final_amount = int(amount * multiplier)
        self.health.current += final_amount

    def append_inventory(self, item_class: ItemType, item_id, amount):
        all_inventories = {
            ItemType.consumable: self.backpack,
            ItemType.weapon: self.weapons,
            ItemType.blessing: self.blessings
        }
        if not (item_id in all_inventories[item_class]):
            all_inventories[item_class][item_id] = 0
        all_inventories[item_class][item_id] += amount

    def regenerate(self):
        self.health.regenerate()
        self.mana.regenerate()
        self.stamina.regenerate()

    async def increase_level(self, ctx, amount):
        levelled = 0
        before = self.level
        self.level_value.current += amount
        while self.level_value.percent() >= 1:
            self.level_value.current -= self.level_value.max
            self.level_value.max += int(self.level_value.max * 0.25)
            self.level += 1
            levelled = True
        if levelled:
            await ctx.send(embed=discord.Embed(
                title=f"Level up! {before} -> {self.level}",
                description=f"{self.level_value.max - self.level_value.current} more points to level {self.level + 1}",
                colour=Dependencies.success_embed_colour
            ))
    # endregion

    # region Statics
    @staticmethod
    def initialize(client):
        BattleProfile.client = client

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
    def fetch_user(user_id, fallback_id):
        batch = [x for x in BattleProfile.collection if x.user_id == user_id]
        if batch:
            return batch[0]
        return [x for x in BattleProfile.collection if x.user_id == fallback_id][0]
    # endregion

    class ActionType(Enum):
        attack = 0
        dodge = 1
        idle = 2


class Enemy:
    # TODO: Make enemies vulnerable to debuffs (poison, bleeding, confusion, etc etc etc)
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

        self.effects = {}

        self.loot_table = {}
        self.coin_reward = data_table['coin_reward']
        self.exp_reward = data_table['exp_reward']
        self.get_loot_table(data_table['loot_table'])

    def get_loot_table(self, data_table):
        # called when new Enemy is created
        # loot table is not saved, a new one is created on startup
        self.loot_table = {
            ItemType.consumable: {},
            ItemType.weapon: {},
            ItemType.blessing: {}
        }
        for item in data_table['consumable'].items():
            self.loot_table[ItemType.consumable][Consumable.get_enum(item[0])] = item[1]

        for item in data_table['weapons'].items():
            self.loot_table[ItemType.weapon][Weapon.get_enum(item[0])] = item[1]
            # self.loot_table[ItemType.weapon].append(Weapon.get_enum(item[0]))

        for item in data_table['blessings'].items():
            self.loot_table[ItemType.blessing][Blessing.get_enum(item[0])] = item[1]
            # self.loot_table[ItemType.blessing].append(Blessing.get_enum(item[0]))

        # self.loot_table[ItemType.weapon] = [Weapon.get_enum(x) for x in data_table['weapons']]
        # self.loot_table[ItemType.blessing] = [Blessing.get_enum(x) for x in data_table['blessings']]

    def is_dead(self):
        return self.health.percent() <= 0

    def fetch_rewards(self):
        return self.loot_table

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
