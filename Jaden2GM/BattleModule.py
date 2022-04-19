# commands and etc for battle

import discord
from discord.ext import commands
import random
import math

import Dependencies
import Formatting

import User
from Game import ItemClass, Battle, StatusEffects
from Game.ItemClass import Consumable
from Game.Battle import BattleProfile, Enemy
from Game.StatusEffects import EffectContainer


def regular_pattern(ctx)->BattleProfile:
    BattleProfile.update_user(ctx.message.author.name, ctx.message.author.id)
    return BattleProfile.fetch_user(ctx.message.author.id, ctx.message.author.id)


def init(client: commands.Bot):
    Enemy.initialize()
    BattleProfile.load()
    BattleProfile.initialize(client)

    @client.event
    async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
        if user.bot:
            return
        matching_profiles = [x for x in BattleProfile.collection if x.user_id == user.id]
        if not matching_profiles:
            return
        profile: BattleProfile = matching_profiles[0]
        if reaction.message.id != profile.enemy_message:
            return
        if reaction.emoji == Battle.battle_reactions['dodge']:
            await profile.progress_game(reaction.message.channel, BattleProfile.ActionType.dodge)
        else:
            index = Battle.battle_reactions['numbers'].index(reaction.emoji)
            await profile.progress_game(reaction.message.channel, BattleProfile.ActionType.attack, index)
        await reaction.remove(user)

    @client.command()
    async def find_fight(ctx):
        profile = regular_pattern(ctx)
        await ctx.message.delete()
        profile.enemies.append(
            Enemy([Enemy.Species.zombie, Enemy.Species.undead_miner, Enemy.Species.goblin][random.randint(0, 2)]))

        await profile.progress_game(ctx, BattleProfile.ActionType.idle)

    @client.command()
    async def stats(ctx):
        profile = regular_pattern(ctx)
        await ctx.message.delete()
        await profile.display_stats(ctx)

    @client.command()
    async def attack(ctx, *args):
        profile = regular_pattern(ctx)
        await ctx.message.delete()

        enemies_alive = len([x for x in profile.enemies if not x.is_dead()])

        if enemies_alive <= 0:
            await profile.progress_game(ctx, BattleProfile.ActionType.attack)
            return

        try:
            index = int(args[0])
            if index > len(profile.enemies):
                raise IndexError
            if index <= 0:
                raise IndexError
            index -= 1
        except IndexError or ValueError:
            await (await ctx.send(embed=discord.Embed(
                title="Invalid input!",
                description=f"Please enter a number between 1 - {len(profile.enemies)}",
                colour=Dependencies.error_embed_colour
            )).delete(delay=3))
            return

        if profile.enemies[index].is_dead():
            await (await ctx.send(embed=discord.Embed(
                title="That enemy is already dead!",
                colour=Dependencies.error_embed_colour
            )).delete(delay=3))
            return

        # await profile.attack(ctx, index)
        await profile.progress_game(ctx, BattleProfile.ActionType.attack, index)

    @client.command()
    async def dodge(ctx, *args):
        profile = regular_pattern(ctx)
        await ctx.message.delete()
        await profile.progress_game(ctx, BattleProfile.ActionType.dodge)

    @client.command()
    async def use(ctx, *args):
        profile = regular_pattern(ctx)

        available = '\n'.join(
            [f"{Consumable.item_symbols[x]} **{Consumable.display_names[x]}**" for x in profile.backpack.keys()])
        final = discord.Embed(
            title="",
            description=f"These are some of the usable items:\n{available}",
            colour=Dependencies.error_embed_colour)
        if not args:
            final.title = "Item name not provided!"
            await ctx.send(embed=final)
            return

        in_message = Formatting.find_argument(ctx.message.content)
        _item_name = in_message[0]
        item_type = [x for x in profile.backpack if Consumable.display_names[x].lower() == _item_name.lower()]
        if not item_type:
            final.title = "Item not found!"
            await ctx.send(embed=final)
            return

        item = Consumable.collection[item_type[0]]
        # amount = in_message[1]
        #
        # if amount <= 0:
        #     amount = 1
        amount = 1

        if amount > profile.backpack[item.item_id]:
            final.title = f'Not enough in inventory!'
            final.description = ''
            await ctx.send(embed=final)
            return

        final.title = f'Used {amount} {item.name}!'
        final.colour = Dependencies.success_embed_colour
        profile.backpack[item.item_id] -= amount

        # profile.health.current += item.health_return
        profile.apply_health(item.health_return)
        for x in item.effects.items():
            profile.apply_effect(x[0], x[1])

        final_description = ''
        if len(item.effects):
            final_description = f'**Effects** : ' + ', '.join(
                [f'{EffectContainer.display_names[x[0]]}[{x[1]}]' for x in item.effects.items()])
        final.description = final_description

        await ctx.message.delete()
        await (await ctx.send(embed=final)).delete(delay=3)
        if len(profile.enemies):
            await profile.progress_game(ctx, BattleProfile.ActionType.idle)
        else:
            await profile.display_stats(ctx)

    @client.command()
    async def inventory(ctx, *args):
        profile = regular_pattern(ctx)

        if ctx.message.mentions:
            profile = BattleProfile.fetch_user(ctx.message.mentions[0].id, ctx.message.author.id)

        if not args:
            page = 0
        else:
            in_message = Formatting.find_argument(ctx.message.content)
            page = in_message[1] + 1

        amount_per_page = 10
        max_page = math.ceil((len(profile.backpack) / amount_per_page) - 1)
        """
        0 - 0-10
        1 - 11-20
        2 - 21-30
        3 - 31-40

        35, p = 3
        """
        if page > max_page:
            page = max_page

        page_content = [i for i in list(profile.backpack.keys())[page * amount_per_page:(page + 1) * amount_per_page]]
        final = ""
        for x in page_content:
            final += f"{Consumable.item_symbols[x]} **{Consumable.display_names[x]}** - {profile.backpack[x]}\n"

        final_embed = discord.Embed(
            title=f"{profile.name}'s Inventory",
            description=f"{final}",
            colour=Formatting.colour()
        )
        final_embed.set_footer(text=f"Page {page + 1}/{max_page + 1}")
        await ctx.message.delete()
        await ctx.send(embed=final_embed)

    @client.command()
    async def blessings(ctx, *args):
        profile = regular_pattern(ctx)

        if ctx.message.mentions:
            profile = BattleProfile.fetch_user(ctx.message.mentions[0].id, ctx.message.author.id)

        if not args:
            page = 0
        else:
            in_message = Formatting.find_argument(ctx.message.content)
            page = in_message[1] + 1

        amount_per_page = 10
        max_page = math.ceil((len(profile.blessings) / amount_per_page) - 1)
        """
        0 - 0-10
        1 - 11-20
        2 - 21-30
        3 - 31-40

        35, p = 3
        """
        if page > max_page:
            page = max_page

        page_content = [i for i in list(profile.blessings.keys())[page * amount_per_page:(page + 1) * amount_per_page]]

        final_embed = discord.Embed(
            title=f"{profile.name}'s Blessings",
            colour=Formatting.colour()
        )

        for x in page_content:
            b = ItemClass.equipment_stats[ItemClass.ItemType.blessing][x.name]
            buffs = '\n'.join([f'_{StatusEffects.PropertyContainer.display_names[x[0]]} : {round(100 * (x[1] - 1), 2)}%_' for x in b['buffs'].items()])
            final_embed.add_field(
                name=f"{ItemClass.equipment_stats['item_symbols'][b['blessing_type']]} {b['name']} - {profile.blessings[x]}",
                value='_' + b['description'] + '_' + (f'\n\n{buffs}' if b['buffs'] else '')
            )

        final_embed.set_footer(text=f"Page {page + 1}/{max_page + 1}")
        await ctx.message.delete()
        await ctx.send(embed=final_embed)

    @client.command()
    async def arsenal(ctx, *args):
        profile = regular_pattern(ctx)

        if ctx.message.mentions:
            profile = BattleProfile.fetch_user(ctx.message.mentions[0].id, ctx.message.author.id)

        if not args:
            page = 0
        else:
            in_message = Formatting.find_argument(ctx.message.content)
            page = in_message[1] + 1

        amount_per_page = 6
        max_page = math.ceil((len(profile.weapons) / amount_per_page) - 1)
        """
        0 - 0-10
        1 - 11-20
        2 - 21-30
        3 - 31-40
    
        35, p = 3
        """
        if page > max_page:
            page = max_page

        final_embed = discord.Embed(
            title=f"{profile.name}'s Arsenal",
            colour=Formatting.colour()
        )

        page_content = [i for i in list(profile.weapons.keys())[page * amount_per_page:(page + 1) * amount_per_page]]
        for x in page_content:
            w = ItemClass.equipment_stats[ItemClass.ItemType.weapon][x.name]
            buffs = '\n'.join([f'_{StatusEffects.PropertyContainer.display_names[x[0]]} : {round(100 * (x[1] - 1), 2)}%_' for x in w['buffs'].items()])
            final_embed.add_field(
                name=f"{ItemClass.equipment_stats['item_symbols'][w['weapon_type']]} {w['name']} - {profile.weapons[x]}",
                value='_' + w['description'] + '_' + (f'\n\n{buffs}' if w['buffs'] else '')
            )

        final_embed.set_footer(text=f"Page {page + 1}/{max_page + 1}")
        await ctx.message.delete()
        await ctx.send(embed=final_embed)

    @client.command()
    async def info(ctx, *args):
        item_name = ' '.join(args)
        item = ItemClass.search_item(item_name)
        if not item:
            await (await ctx.send(embed=discord.Embed(
                title=f'Item with name "{item_name}" could not be found.',
                description='Make sure to input the exact name.',
                colour=Dependencies.error_embed_colour
            ))).delete(delay=3)
            return
        data = item[1]
        final_embed = discord.Embed(
            title=data['name']
        )
        if item[0] == ItemClass.ItemType.weapon:
            final_embed.description = f"_{data['description']}_\n\n" \
                                      f"**Type   :** {ItemClass.equipment_stats['item_symbols'][data['weapon_type']]} {ItemClass.equipment_stats['type_names'][data['weapon_type']]}\n" \
                                      f"**Rarity :** {str(data['rarity']).capitalize()}\n" \
                                      f"**Elements :** {' '.join([ItemClass.equipment_stats['element_symbols'][x] for x in data['elements']]) if data['elements'] else '_None_'}\n" \
                                      f"\n" \
                                      f"**Damage :** `{data['damage']}` | **Crit chance :** `{data['crit_rate']}`\n" \
                                      f"**Mana usage :** `{data['mana_usage']}` | **Stamina usage :** `{data['stamina_usage']}`"
            if data['buffs']:
                final_embed.add_field(name='Buffs', value='\n'.join([f' 🞄 _{StatusEffects.PropertyContainer.display_names[x[0]]} : {round(100 * (x[1] - 1))}%_' for x in data['buffs'].items()]))
            final_embed.colour = ItemClass.equipment_stats['rarity_colours'][data['rarity']]
        elif item[0] == ItemClass.ItemType.blessing:
            final_embed.description = f"_{data['description']}_\n\n" \
                                      f"**Type   :** {ItemClass.equipment_stats['item_symbols'][data['blessing_type']]} {ItemClass.equipment_stats['type_names'][data['blessing_type']]}\n" \
                                      f"**Rarity :** {str(data['rarity']).capitalize()}\n" \
                                      f"**Elements :** {' '.join([ItemClass.equipment_stats['element_symbols'][x] for x in data['elements']]) if data['elements'] else '_None_'}\n"
            if data['buffs']:
                final_embed.add_field(name='Buffs', value='\n'.join([f' 🞄 _{StatusEffects.PropertyContainer.display_names[x[0]]} : {round(100 * (x[1] - 1))}%_' for x in data['buffs'].items()]))
            final_embed.colour = ItemClass.equipment_stats['rarity_colours'][data['rarity']]
        else:
            pass
        await ctx.send(embed=final_embed)

    @client.command()
    async def equip_weapon(ctx, *args):
        profile = regular_pattern(ctx)

        if not args:
            await ctx.send(embed=discord.Embed(
                title="No argument provided.",
                colour=Dependencies.error_embed_colour
            ))
            return
        item_name = ' '.join(args)
        item = ItemClass.search_item(item_name)
        if (not item) or (item[0] != ItemClass.ItemType.weapon):
            await ctx.send(embed=discord.Embed(
                title=f"No weapon found with the name \"{item_name}\"",
                description=(f"_Did you mean :_\n"+'\n'.join([f' **{ItemClass.equipment_stats["item_symbols"][ItemClass.equipment_stats[ItemClass.ItemType.weapon][x.name]["weapon_type"]]} {ItemClass.equipment_stats[ItemClass.ItemType.weapon][x.name]["name"]}**' for x in profile.weapons.keys() if (x.name[0].lower() == item_name.lower()[0])])) if (len([x for x in profile.weapons.keys() if (x.name[0] == item_name.lower()[0])])) else '',
                colour=Dependencies.default_embed_colour
            ))
            return
        weapon_type = ItemClass.Weapon.get_enum(item[1]['item_id'])
        if (not (weapon_type in profile.weapons)) or (not (profile.weapons[weapon_type] > 0)):
            await ctx.send(embed=discord.Embed(
                title=f'You don\'t have a "{ItemClass.equipment_stats[ItemClass.ItemType.weapon][weapon_type.name]["name"]}" in your inventory.',
                colour=Dependencies.error_embed_colour
            ))
            return

        # Unequip current weapon
        if profile.current_weapon:
            profile.weapons[profile.current_weapon.item_id] += 1

        # Equip new weapon
        profile.current_weapon = ItemClass.Weapon(weapon_type)
        profile.weapons[profile.current_weapon.item_id] -= 1
        await ctx.send(embed=discord.Embed(
            title=f'{profile.current_weapon.name} equipped',
            colour=Dependencies.success_embed_colour
        ))
