import sys
from . import Task
from . import Item
from . import Experience
import Dependencies
import pickle

sys.path.append("..")


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
                await self.exp.add_exp(ctx, x.exp_reward)
                for reward in x.item_reward:
                    self.inventory.add(reward)

                if send:
                    await Task.Task.announce_task(ctx, x)

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
        await _user.update_user_tasks(ctx, send=send)

    @staticmethod
    def load_all():
        # Loading code here
        pass

    @staticmethod
    def save_all():
        # Saving code here
        pass

    @staticmethod
    def startup():  # Function called on startup
        User.load_all()
