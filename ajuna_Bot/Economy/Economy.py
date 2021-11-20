import sys
from . import User
from . import Task
import Formatting
import discord
from discord.ext import commands
sys.path.append("..")

"""
sooo @🅰jian_nedo | Godly @n🅾 i have an idea about bringing a coin system here
a shop, rewards, achievements, tasks etc
rewards, achievements, reputation, tasks
"""


def init(client):
    @client.event
    async def on_message(message):
        if message.author.bot:
            return

        User.User.update_user_data(message.author.id, message.author.name)

        User.User.update_progress(
            User.User.users[message.author.id],
            Task.Task.TaskType.Message,
            1
        )

        await client.process_commands(message)

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
        await ctx.send(embed=final)

    @client.command()
    async def task_select(ctx, args="none"):
        Task.Task.update_task_log()
        if args != "none":
            try:
                _index = int(args)
                _task = Task.Task.task_log[_index - 1]
                _user = User.User.users[ctx.message.author.id]

                _user.tasks.append(_task)
                Task.Task.task_log.remove(_task)
                final = discord.Embed(title="**Task Added Successfully!**",
                                      description=f"_Task :_ **{_task.title}** `({_task.coin_reward}c {_task.exp_reward}xp)`",
                                      color=Formatting.colour()
                                      )
                await ctx.send(embed=final)
                return
            except:
                pass

        # • ```{c}c ```{xp}xp {title}
        final = discord.Embed(title="Task Selection List", description='\n'.join([
            f"`{x[0] + 1}.` `{str(x[1].coin_reward).rjust(3,' ')}c {str(x[1].exp_reward).rjust(4, ' ')}xp` {x[1].title}"
            for x in enumerate(Task.Task.task_log)]), color=Formatting.colour())
        await ctx.send(embed=final)
