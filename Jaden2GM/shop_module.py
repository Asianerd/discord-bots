import discord
import Formatting
import game
import User
import Dependencies

from game import Consumable
from game import Equipment


class Shop:
    selling = {
        game.ItemType.equipment: [
            Consumable.ItemID.bread,
            Consumable.ItemID.apple,
            Consumable.ItemID.apple_pie,
            Consumable.ItemID.golden_apple,

            Consumable.ItemID.ironskin_potion,
            Consumable.ItemID.wrath_potion,
            Consumable.ItemID.adrenaline_vial
        ],
        game.ItemType.consumable: [
            Equipment.ItemID.iron_shortsword,
            Equipment.ItemID.platinum_shortsword,
        ]
    }


def get_item(name):
    # returns a list of all items with same name
    return [x for x in game.all_collections() if x.name.lower() == name.lower()]


def find_argument(message: str):
    """
    0: content
    1: amount
    """
    amount = 1
    final = []
    for x in message.split(" "):
        if x.isdigit():
            try:
                amount = int(x)
            except ValueError:
                pass
        else:
            final.append(x)
    return [' '.join(final[1:]), amount]


def init(client):
    game.initialize()

    @client.command()
    async def shop(ctx, args=''):
        final = '\n'.join([x.readable() for x in Consumable.collection.values()])
        await ctx.send(embed=discord.Embed(title="Shop", description=final, colour=Formatting.colour()))

    @client.command()
    async def buy(ctx, *args):
        if not args:
            await ctx.send(embed=discord.Embed(
                title="No item name given.",
                description="Use `>shop` to view all the  items.",
                colour=Formatting.colour()
            ))
            return

        in_message = find_argument(ctx.message.content)

        # name = ' '.join(args[0:-1]).lower() if len(args) >= 2 else args[0].lower()

        name, amount = in_message

        result = get_item(name)
        if not result:
            suggestions = [f"_{x.name}_   - ${x.price}" for x in game.all_collections() if name[0] == x.name[0].lower()]
            await ctx.send(embed=discord.Embed(
                title=f"No items with the name '{name}' were found.",
                description=f"Did you mean :\n" + '\n'.join(
                    suggestions) if suggestions else 'Please use `>shop` to view all the items.',
                colour=Formatting.colour()
            ))
            return

        user: User.User = [x for x in User.User.users if x.user_id == ctx.message.author.id][0]
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

        user.append_inventory(item_result.item_id, game.ItemType.consumable, amount)
        user.points -= price
        await ctx.send(embed=discord.Embed(
            title=f"Bought {amount} {item_result.name}",
            description=f"{user.points + price} -> {user.points}",
            colour=Dependencies.success_embed_colour
        ))
