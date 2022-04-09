import discord
import math

import Formatting
import User
import Dependencies

from Game import ItemClass
from Game.ItemClass import Consumable, Weapon, Blessing, ItemType
from Game.Battle import BattleProfile


class Shop:
    selling = [
        Consumable.ItemID.bread,
        Consumable.ItemID.apple,
        Consumable.ItemID.apple_pie,
        Consumable.ItemID.golden_apple,

        Consumable.ItemID.ironskin_potion,
        Consumable.ItemID.wrath_potion,
        Consumable.ItemID.adrenaline_vial
    ]


def get_item(name):
    # returns a list of all items with same name
    return [x for x in ItemClass.Consumable.collection.values() if x.name.lower() == name.lower()]


def init(client):
    ItemClass.initialize()

    @client.command()
    async def shop(ctx, *args):
        page = Formatting.find_argument(ctx.message.content)[1] - 1
        amount_per_page = 4
        if page < 0:
            page = 1

        max_page = math.ceil((len(Shop.selling) / amount_per_page) - 1)
        if page > max_page:
            page = max_page

        final_embed = discord.Embed(
            title="Shop",
            colour=Formatting.colour()
        )

        page_data = Shop.selling[(amount_per_page * page):(amount_per_page * (page + 1))]
        page_data = [page_data[0:int(amount_per_page/2)], page_data[int(amount_per_page/2):]]
        for i in page_data:
            final = ''
            for x in i:
                final += ItemClass.Consumable.collection[x].readable() + '\n'
            final_embed.add_field(name='Items', value=final)

        final_embed.set_footer(text=f'Page {page+1}/{max_page+1}')
        await ctx.send(embed=final_embed)

    @client.command()
    async def buy(ctx, *args):
        if not args:
            await ctx.send(embed=discord.Embed(
                title="No item name given.",
                description="Use `>shop` to view all the  items.",
                colour=Formatting.colour()
            ))
            return

        in_message = Formatting.find_argument(ctx.message.content)

        # name = ' '.join(args[0:-1]).lower() if len(args) >= 2 else args[0].lower()

        name, amount = in_message

        result = get_item(name)
        if not result:
            suggestions = [f"_{x.name}_   - ${x.price}" for x in ItemClass.Consumable.collection.items() if name[0] == x.name[0].lower()]
            await ctx.send(embed=discord.Embed(
                title=f"No items with the name '{name}' were found.",
                description=f"Did you mean :\n" + '\n'.join(
                    suggestions) if suggestions else 'Please use `>shop` to view all the items.',
                colour=Formatting.colour()
            ))
            return

        user: User.User = [x for x in User.User.users if x.user_id == ctx.message.author.id][0]
        profile: BattleProfile = BattleProfile.fetch_user(ctx.message.author.id, ctx.message.author.id)
        item_result = result[0]

        # if len(args) >= 2:
        #     amount = 1
        #     for i in args:
        #         try:
        #             amount = int(i)
        #             break
        #         except ValueError:
        #             continue
        # else:
        #     amount = 1
        if amount <= 0:
            amount = 1

        price = item_result.price * amount

        if user.points < price:
            await ctx.send(embed=discord.Embed(
                title="You don't have enough money!",
                description=f"You need {price - user.points} more coins!",
                colour=Dependencies.error_embed_colour
            ))
            return

        # user.append_inventory(item_result.item_id, ItemClass.ItemType.consumable, amount)
        profile.append_inventory(ItemType.consumable, item_result.item_id, amount)
        user.points -= price
        await ctx.send(embed=discord.Embed(
            title=f"Bought {amount} {item_result.name}",
            description=f"{user.points + price} -> {user.points}",
            colour=Dependencies.success_embed_colour
        ))
