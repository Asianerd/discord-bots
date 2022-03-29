# commands and etc for battle

import discord
import random

import Dependencies
import Formatting

import User
from Game import ItemClass, Battle
from Game.ItemClass import Consumable
from Game.Battle import BattleProfile, Enemy


def regular_pattern(ctx):
    BattleProfile.update_user(ctx.message.author.name, ctx.message.author.id)
    return BattleProfile.fetch_user(ctx.message.author.id)


def init(client):
    Enemy.initialize()
    BattleProfile.load()

    @client.command()
    async def find_fight(ctx):
        profile = regular_pattern(ctx)
        profile.enemies.append(Enemy([Enemy.Species.zombie, Enemy.Species.undead_miner, Enemy.Species.goblin][random.randint(0, 2)]))

        await profile.progress_game(ctx)

    @client.command()
    async def stats(ctx):
        profile = regular_pattern(ctx)
        await profile.display_stats(ctx)

    @client.command()
    async def attack(ctx, *args):
        profile = regular_pattern(ctx)

        # if len(profile.enemies) == 1:
        #     profile.attack(0)
        # else:
        #     if not args:
        #         await ctx.send(embed=discord.Embed(
        #             title="Invalid input!",
        #             description=f"Please enter a number between 1 - {len(profile.enemies)}"
        #         ))
        #         return
        #     else:
        #         try:
        #             index = int(args[0])
        #         except ValueError:
        #             await ctx.send(embed=discord.Embed(
        #                 title="Invalid input!",
        #                 description=f"Please enter a number between 1 - {len(profile.enemies)}"
        #             ))
        #             return

        enemies_alive = len([x for x in profile.enemies if not x.is_dead()])

        if enemies_alive <= 0:
            await profile.progress_game(ctx)
            return

        try:
            index = int(args[0])
            if index > len(profile.enemies):
                raise IndexError
            if index <= 0:
                raise IndexError
            index -= 1
        except Exception as e:
            await ctx.send(embed=discord.Embed(
                title="Invalid input!",
                description=f"Please enter a number between 1 - {len(profile.enemies)}",
                colour=Dependencies.error_embed_colour
            ))
            return

        if profile.enemies[index].is_dead():
            await ctx.send(embed=discord.Embed(
                title="That enemy is already dead!",
                colour=Dependencies.error_embed_colour
            ))
            return

        await profile.attack(ctx, index)
        await profile.progress_game(ctx)

    @client.command()
    async def dodge(ctx):
        profile = regular_pattern(ctx)

        await profile.progress_game(ctx)
        await ctx.send("dodge")

    @client.command()
    async def use(ctx, *args):
        profile = regular_pattern(ctx)

        user = User.User.fetch_user(ctx.message.author.id, ctx.message.author.name)
        available = '\n'.join(
            [f"{Consumable.item_symbols[Consumable.get_enum(x)]} **{Consumable.display_names[Consumable.get_enum(x)]}**" for x in
             user.inventory[ItemClass.ItemType.consumable.name].keys()])
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
        item_type = [Consumable.get_enum(x) for x in user.inventory[ItemClass.ItemType.consumable.name] if Consumable.display_names[Consumable.get_enum(x)].lower() == _item_name.lower()]
        if not item_type:
            final.title = "Item not found!"
            await ctx.send(embed=final)
            return

        item = Consumable.collection[item_type[0]]
        amount = in_message[1]

        if amount <= 0:
            amount = 1

        if amount > user.inventory[ItemClass.ItemType.consumable.name][item.item_id.name]:
            final.title = f'Not enough in inventory!'
            final.description = ''
            await ctx.send(embed=final)
            return

        final.title = f'Used {amount} {item.name}!'
        final.description = ''
        final.colour = Dependencies.success_embed_colour
        user.inventory[ItemClass.ItemType.consumable.name][item.item_id.name] -= amount

        #profile.health.current += item.health_return
        profile.apply_health(item.health_return)
        for x in item.effects.items():
            profile.apply_effect(x[0], x[1])

        await ctx.send(embed=final)
        await profile.display_stats(ctx)
