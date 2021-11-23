import sys
import math
from . import User
from . import Task
from . import Item
import Formatting
import Dependencies
import discord

sys.path.append("..")

"""
sooo @🅰jian_nedo | Godly @n🅾 i have an idea about bringing a coin system here
a shop, rewards, achievements, tasks etc
rewards, reputation

- Shop          (wip)
- Rewards
- Achievements
- Tasks         (done)
- Reputation
"""


def select_next_few(iterable, amount, start):
    final = []
    selection_range = range(start, start + amount)
    for x in enumerate(iterable):
        if x[0] in selection_range:
            final.append(x[1])
    return final


async def on_message(client, message):
    if message.author.bot:
        return

    User.User.update_user_data(message.author.id, message.author.name)

    await User.User.update_progress(
        message.channel,
        User.User.users[message.author.id],
        Task.TaskType.Message,
        1
    )

    if message.content:
        if Dependencies.is_valid_english(message.content.split()[0]):
            await User.User.users[message.author.id].exp.add_exp(message.channel, 1)

    # await client.process_commands(message)


async def on_reaction_add(client, reaction, _user):
    if _user.bot:
        return

    User.User.update_user_data(_user.id, _user.name)

    await User.User.update_progress(
        reaction.message.channel,
        User.User.users[_user.id],
        Task.TaskType.Reaction,
        1
    )


async def on_voice_state_update(client, member, before, after):
    if not after.channel:
        return
    User.User.update_user_data(member.id, member.name)
    await User.User.update_progress(
        0,
        User.User.users[member.id],
        Task.TaskType.Voice_channel,
        1,
        send=False
    )
    # No text channel to send the task announcement to


def init(client):
    @client.command()
    async def tasks(ctx, index="none"):
        _fetched_user = User.User.users[ctx.message.author.id]

        title = "**Tasks**"
        message = _fetched_user.get_tasks()

        if index != "none":
            try:
                wanted_index = int(index)
                _fetched_task = _fetched_user.tasks[wanted_index]
                message = f"`[{_fetched_task.progress}/{_fetched_task.max}]`" \
                          f"{int(_fetched_task.progress_percentage() * 100)}%\n" \
                          f"\n" \
                          f"**Coin : {_fetched_task.coin_reward}\n" \
                          f"Exp  : {_fetched_task.exp_reward}**"
                title = f"**{_fetched_task.title}**"
            except:
                await ctx.send("Invalid value entered. Please re-enter")
                return

        final = discord.Embed(title=title, description=message, color=Formatting.colour())
        await ctx.send(embed=final)

    @client.command()
    async def profile(ctx):
        _user = User.User.users[ctx.message.author.id]
        final = discord.Embed(title=_user.username, description=_user.profile(), color=Formatting.colour())
        await Dependencies.dispose_message(await ctx.send(embed=final))

    @client.command()
    async def task_select(ctx, args="none"):
        Task.Task.update_task_log()
        if args != "none":
            if await Task.Task.select_task(ctx, args):
                return

        # • ```{c}c ```{xp}xp {title}
        final = discord.Embed(title="Task Selection List", description='\n'.join([
            f"`{x[0] + 1}.` `{str(x[1].coin_reward).rjust(3, ' ')}c {str(x[1].exp_reward).rjust(4, ' ')}xp` {x[1].title}"
            for x in enumerate(Task.Task.task_log)]), color=Formatting.colour())
        await ctx.send(embed=final)

    @client.command()
    async def inventory(ctx):
        final = discord.Embed(
            title=f"{ctx.message.author}'s Inventory",
            description=User.User.users[ctx.message.author.id].inventory.wording(),
            color=Formatting.colour()
        )
        await Dependencies.dispose_message(await ctx.send(embed=final))
    
    @client.command()
    async def shop(ctx, args="1"):
        await ctx.message.delete()
        try:
            page = int(args) - 1
        except ValueError:
            await ctx.send("Invalid input entered.")
            return

        bs = '\\'
        item_per_page = 5
        page_items = select_next_few(list(Item.Item.item_data.keys()), item_per_page, page * item_per_page)
        if len(page_items) <= 0:
            await (await ctx.send(embed=discord.Embed(
                title="Out of range!",
                color=Formatting.colour()
            ))).delete(delay=3)
            return

        _description = ''
        for x in page_items:
            _item = Item.Item.item_data[x]
            _description += f"**{_item['emoji']} {_item['name'].replace('_',f'{bs}_')}**  - {_item['value']}c\n"\
                            f"- _{str(_item['description']).replace('_',f'{bs}_')}_\n\n"
        final = discord.Embed(
            title="Shop",
            description=_description,
            color=Formatting.colour()
        )
        final.set_footer(text=f"Page {page + 1} of {int(math.ceil(len(Item.Item.item_data)/item_per_page))}")
        await Dependencies.dispose_message(await ctx.send(embed=final))

    @client.command()
    async def buy(ctx, *args):
        await ctx.message.delete()
        try:
            if len(args) >= 2:
                amount = int(args[1])
            else:
                amount = 1
            if amount <= 0:
                await (await ctx.send(embed=discord.Embed(title="bruh", color=Formatting.colour()))).delete(delay=3)
                return
        except:
            await ctx.send(embed=discord.Embed(
                title="Invalid input entered. Please re-enter.",
                color=Formatting.colour()
            ))
            return
        key_names = [(str(x[1]).lower().split('.')[-1], x[0]) for x in enumerate(list(Item.Item.item_data.keys()))]
        if args[0].lower() in [x[0] for x in key_names]:
            _item_str = list(Item.Item.item_data.keys())[[x[1] for x in key_names if x[0] == args[0].lower()][0]]
            _item_type = [x for x in Item.ItemType if str(_item_str).split('.')[-1] == x.name][0]
            _item = Item.Item.item_data[str(_item_type)]
            _user = User.User.users[ctx.message.author.id]
            if _user.coins >= (_item['value'] * amount):
                await ctx.send(embed=discord.Embed(title="Purchase succesful!", description=f"{_item['emoji']} {amount} {_item['name']}{('s' if amount > 1 else '')}", color=Formatting.colour()))
                _user.inventory.add(_item_type, amount)
                _user.coins -= (_item['value'] * amount)
            else:
                await ctx.send(embed=discord.Embed(title="You don't have enough coins.", color=Formatting.colour()))
        else:
            await (await ctx.send(embed=discord.Embed(
                title="Item doesn't exist. Please check the shop for the item names.",
                color=Formatting.colour()
            ))).delete(delay=3)

    @client.command()
    async def global_ranking(ctx):
        newline = "\n"
        apos = "'"
        final = discord.Embed(
            title="Rankings",
            color=Formatting.colour()
        )
        users = list(User.User.users.values())
        users.sort(key=(lambda x: x.exp.total), reverse=True)
        final.add_field(name="**Exp ranks**",
                        value=
                        f"```txt\n{newline.join([f'{str(x.exp.total).rjust(5, apos)} {x.username}' for x in users[0:10]])}\n```"
                        )

        users.sort(key=(lambda x: x.coins), reverse=True)
        final.add_field(name="**Coin ranks**",
                        value=
                        f"```txt\n{newline.join([f'{str(x.coins).rjust(5, apos)} {x.username}' for x in users[0:10]])}\n```"
                        )
        await ctx.send(embed=final)


