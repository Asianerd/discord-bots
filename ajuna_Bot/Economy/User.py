import sys
from . import Task
from . import Item
from . import Experience
import Dependencies
import pickle
import json

sys.path.append("..")


def append_data(user_id, new):
    data = json.load(open("users.json", "r"))
    data[str(user_id)] = new[str(user_id)]
    json.dump(data, open("users.json", "w"))


class User:
    users = {}

    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.coins = 0
        self.exp = Experience.Experience()
        self.tasks = []
        self.completed_tasks = []
        self.inventory = Item.Inventory()

    def get_tasks(self):
        if len(self.tasks) <= 0:
            return "You have no tasks!"
        else:
            return "\n".join([f"• {x.wording()}" for x in self.tasks])

    def profile(self):
        return f"""
        **Level {self.exp.level}**  `{self.exp.current}/{self.exp.next_level_requirement}`
        **Coins : {self.coins}**
        **Tasks completed : {len(self.tasks)}**
        """

    def add_task(self, task):
        self.tasks.append(task)

    async def update_user_tasks(self, ctx, send):
        if len(self.tasks) <= 0:
            return
        for x in self.tasks.copy():
            if x.completed:
                self.completed_tasks.append(x)
                self.tasks.remove(x)
                self.coins += x.coin_reward
                await self.exp.add_exp(ctx, x.exp_reward, send=send)
                for reward in x.item_reward:
                    self.inventory.add(reward)

                if send:
                    await Task.Task.announce_task(ctx, x)

    def to_json(self):
        return {
            str(self.user_id): {
                'user_id': self.user_id,
                'username': self.username,
                'coins': self.coins,
                'exp': self.exp.to_json(),
                'tasks': [x.to_json() for x in self.tasks],
                'completed_tasks': [x.to_json() for x in self.completed_tasks],
                'inventory': self.inventory.to_json()
            }
        }

    def from_json(self, data):
        self.user_id = data['user_id']
        self.username = data['username']
        self.coins = data['coins']

        self.exp = Experience.Experience()
        self.exp.from_json(data['exp'])

        # self.tasks = [Task.Task(Task.TaskType.Message, 0, 0) for x in data['tasks']]
        self.tasks = []
        for x in data['tasks']:
            self.tasks.append(Task.Task(Task.TaskType.Message, 0, 0))
            self.tasks[-1].from_json(x)

        self.completed_tasks = []
        for x in data['completed_tasks']:
            self.completed_tasks.append(Task.Task(Task.TaskType.Message, 0, 0))
            self.completed_tasks[-1].from_json(x)

        self.inventory = Item.Inventory()
        self.inventory.from_json(data['inventory'])


    """Static section"""
    @staticmethod
    def update_user_data(user_id, current_username):  # Called everytime a message, reaction or voice channel event happens
        if user_id in [x.user_id for x in User.users.values()]:
            # Update the user's data (name, etc)
            user = User.users[user_id]
            user.username = current_username
        else:
            # Create new user and append to list
            User.users[user_id] = User(user_id, current_username)
        User.save_all()

    @staticmethod
    async def update_progress(ctx, _user, _type, _amount, send=True):
        _collection = [x for x in _user.tasks if x.type == _type]
        for x in _collection:
            x.update_progress(_amount)
        await _user.update_user_tasks(ctx=ctx, send=send)

    @staticmethod
    def load_all():
        data = json.load(open("users.json", "r"))
        for x in data.keys():
            _user = data[x]
            User.update_user_data(int(_user['user_id']), _user['username'])
            User.users[int(x)].from_json(_user)

    @staticmethod
    def save_all():
        for x in User.users.values():
            append_data(x.user_id, x.to_json())

    @staticmethod
    def startup():  # Function called on startup
        User.load_all()
