import sys
from enum import Enum
from . import Item
from . import User
import random
import discord
import Formatting
sys.path.append("..")


class Task:
    task_selection_message = 0
    task_log = []

    class TaskType(Enum):
        Message = 0
        Reaction = 1
        Voice_channel = 2

    task_type_amount = {
        TaskType.Message: 10,
        TaskType.Reaction: 3,
        TaskType.Voice_channel: 1
    }

    task_type_coin_amount = {
        TaskType.Message: 2,    # (for message related tasks) one message = 1 * 2 coin
        TaskType.Reaction: 1,
        TaskType.Voice_channel: 5
    }

    task_type_exp_amount = {
        TaskType.Message: 10,   # (for message related tasks) one message = 1 * 10 exp
        TaskType.Reaction: 8,
        TaskType.Voice_channel: 15
    }

    """
        Cookie = 0
        Tea = 1
        billy_os = 2
        PP_yes = 3
        ajian_bat = 4
    """
    task_type_item_reward = {
        TaskType.Message:[Item.Item.ItemType.Cookie, Item.Item.ItemType.billy_os],
        TaskType.Reaction:[Item.Item.ItemType.Tea, Item.Item.ItemType.PP_yes],
        TaskType.Voice_channel:[Item.Item.ItemType.Cookie, Item.Item.ItemType.ajian_bat],
    }

    def __init__(self, _type, title, _max, level):
        self.title = title
        self.type = _type

        self.max = _max
        self.progress = 0

        self.completed = False

        self.coin_reward = Task.task_type_coin_amount[_type] * self.max
        self.exp_reward = Task.task_type_exp_amount[_type] * self.max
        self.item_reward = [Task.task_type_item_reward[self.type]
                            [random.randint(0, len(Task.task_type_item_reward[self.type]) - 1)]
                            for x in range(level)]

    def update_progress(self, amount):
        self.progress += amount
        self.completion_check()

    def completion_check(self):
        if self.progress >= self.max:
            self.completed = True

    # Please rename this into something better
    def wording(self):
        return f"**[{self.progress}/{self.max}]** {self.title}"

    def progress_percentage(self):
        return self.progress / self.max

    """Static methods"""
    @staticmethod
    def update_task_log():
        if len(Task.task_log) > 5:
            Task.task_log = Task.task_log[0:4]
        elif len(Task.task_log) < 5:
            for x in range(5 - len(Task.task_log)):
                Task.task_log.append(Task.generate_task(random.randint(1, 4)))

        Task.task_log.sort(key=(lambda n: n.exp_reward))

    @staticmethod
    def generate_task(level):
        _type = Task.TaskType(random.randint(0, len(Task.TaskType)-1))
        _amount = Task.task_type_amount[_type] * (2 ** level)
        return Task(_type, f"{({Task.TaskType.Message:'Send', Task.TaskType.Reaction:'Add', Task.TaskType.Voice_channel:'Join'}[_type])} "
                           f"{_amount} "
                           f"{({Task.TaskType.Message:'messages', Task.TaskType.Reaction:'reactions', Task.TaskType.Voice_channel:'voice channels'}[_type])}", _amount, level)

    @staticmethod
    async def announce_task(ctx, task):
        final = discord.Embed(
            title="Task completed!",
            description=f"_{task.title}_ : Completed\n"
                        f"`{f'+{task.coin_reward}c'.rjust(4, ' ')} {f'+{task.exp_reward}'.rjust(4, ' ')}xp`\n"
                        f"+ {', '.join([x.name for x in task.item_reward])}",
            color=Formatting.colour()
        )
        await (await ctx.send(embed=final)).delete(delay=3)

    @staticmethod
    async def select_task(ctx, args):
        try:
            _index = int(args)
            _task = Task.task_log[_index - 1]
            _user = User.User.users[ctx.message.author.id]

            _user.tasks.append(_task)
            Task.task_log.remove(_task)
            final = discord.Embed(title="**Task Added Successfully!**",
                                  description=f"_Task :_ **{_task.title}** `({_task.coin_reward}c {_task.exp_reward}xp)`",
                                  color=Formatting.colour()
                                  )
            await ctx.send(embed=final)
            return True
        except Exception as e:
            print(e)
            return False
