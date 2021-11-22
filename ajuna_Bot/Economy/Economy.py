import sys
from . import User
from . import Task
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

    # await client.process_commands(message)


async def on_reaction_add(client, reaction, _user):
    if _user.bot:
        return
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
    async def reroll_tasks(ctx):
        await ctx.message.delete()
        Task.Task.task_log = []
        Task.Task.update_task_log()
        await task_select(ctx)
