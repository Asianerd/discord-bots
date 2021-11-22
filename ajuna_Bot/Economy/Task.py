import sys
import json
from enum import Enum
from . import Item
from . import User
import random
import discord
import Formatting
sys.path.append("..")


class TaskType(Enum):
    Message = 0
    Reaction = 1
    Voice_channel = 2


class Task:
    task_log = []
    task_data = {}

    def __init__(self, _type, _max, level):
        self.type = _type

        self.max = _max
        self.progress = 0

        self.completed = False

        _task = Task.task_data[str(self.type)]
        self.title = str(_task["title"]).format(str(self.max))

        self.coin_reward = _task["coin"] * _task["amount"]
        self.exp_reward = _task["exp"] * _task["amount"]
        self.item_reward = []
        for x in range(level):
            _item = _task["items"][random.randint(0, len(_task["items"]) - 1)]
            self.item_reward.append([x for x in Item.ItemType if x.name == _item][0])


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
    def initialize():
        Task.task_data = json.load(open("Economy/task_data.json"))

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
        _type = TaskType(random.randint(0, len(TaskType)-1))
        # _amount = Task.task_type_amount[_type] * (2 ** level)
        _amount = Task.task_data[str(_type)]["amount"] * (2 ** level)
        return Task(_type, _amount, level)

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
