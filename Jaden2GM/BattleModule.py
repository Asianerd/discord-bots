# commands and etc for battle

import discord

import Dependencies
import Formatting

import User
from Game import ItemClass, Battle
from Game.ItemClass import Consumable
from Game.Battle import BattleProfile


def init(client):
    BattleProfile.load()

    @client.command()
    async def stats(ctx):
        BattleProfile.update_user(ctx.message.author.name, ctx.message.author.id)
        profile = BattleProfile.fetch_user(ctx.message.author.id)

        await profile.display_stats(ctx)

    @client.command()
    async def attack(ctx):
        BattleProfile.update_user(ctx.message.author.name, ctx.message.author.id)
        await ctx.send("attack")

    @client.command()
    async def dodge(ctx):
        BattleProfile.update_user(ctx.message.author.name, ctx.message.author.id)
        await ctx.send("dodge")

    @client.command()
    async def use(ctx, *args):
        BattleProfile.update_user(ctx.message.author.name, ctx.message.author.id)

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
        await ctx.send(embed=final)