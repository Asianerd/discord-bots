from enum import Enum
import random


class Task:
    task_log = []

    class TaskType(Enum):
        Message = 0
        Reaction = 1

    task_type_amount = {
        TaskType.Message: 10,
        TaskType.Reaction: 3
    }

    task_type_coin_amount = {
        TaskType.Message: 2,    # (for message related tasks) one message = 1 * 2 coin
        TaskType.Reaction: 1
    }

    task_type_exp_amount = {
        TaskType.Message: 10,   # (for message related tasks) one message = 1 * 10 exp
        TaskType.Reaction: 8
    }

    def __init__(self, _type, title, _max):
        self.title = title
        self.type = _type

        self.max = _max
        self.progress = 0

        self.completed = False

        self.coin_reward = Task.task_type_coin_amount[_type] * self.max
        self.exp_reward = Task.task_type_exp_amount[_type] * self.max

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
                Task.task_log.append(Task.generate_task(random.randint(1, 3)))

        Task.task_log.sort(key=(lambda x: x.exp_reward))

    @staticmethod
    def generate_task(level):
        _type = Task.TaskType(random.randint(0, len(Task.TaskType)-1))
        _amount = Task.task_type_amount[_type] * (2 ** level)
        return Task(_type, f"{({Task.TaskType.Message:'Send', Task.TaskType.Reaction:'Add'}[_type])} "
                           f"{_amount} "
                           f"{({Task.TaskType.Message:'messages', Task.TaskType.Reaction:'reactions'}[_type])}", _amount)
