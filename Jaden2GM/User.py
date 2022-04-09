import json
import time
import Quest
from Game import ItemClass


class User:
    users = []
    daily_length = 43200

    @staticmethod
    def initialize():
        User.users = []
        User.load()

    @staticmethod
    def save():
        final = {}
        for x in User.users:
            final[str(x.user_id)] = x.__dict__
        with open('Data/users.json', 'w', encoding='utf-8') as file:
            json.dump(final, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load():
        User.users = []
        with open('Data/users.json', 'r', encoding='utf-8') as file:
            data_file = json.load(file)
            for x in data_file.items():
                data = x[1]

                item = User('', 0)
                item.__dict__ = data
        User.save()

    @staticmethod
    def fetch_user(target_id, username):
        if target_id in [x.user_id for x in User.users]:
            return [x for x in User.users if x.user_id == target_id][0]
        else:
            x = User(username, target_id)
            return x

    def __init__(self, username, user_id):
        if user_id in [x.user_id for x in User.users]:
            return

        self.username = str(username[0:32])
        self.user_id = user_id

        self.points = 0
        self.last_daily_points = 0
        self.streak = 0

        User.users.append(self)

    def update_name(self, name):
        self.username = str(name[0:32])
        User.save()

    def quests_completed(self):
        return len([x for x in Quest.Quest.quests if self.user_id in x.users_completed])

    def daily_points(self):
        if (int(time.time()) - self.last_daily_points) >= User.daily_length:

            if (int(time.time()) - self.last_daily_points) <= (User.daily_length * 2):
                self.streak += 1
            else:
                self.streak = 0

            self.points += 5 + self.streak
            self.last_daily_points = int(time.time())

            if self.streak >= 30:
                self.streak = 0
            return True
        return False

    # def append_inventory(self, _type, _class, amount):
    #     key = str(_type.name)           # Eg. Bread, Apple pie
    #     class_type = str(_class.name)   # Eg. Equipment, Consumables
    #     #class_type = _class   # Eg. Equipment, Consumables
    #
    #     if not (key in self.inventory[class_type].keys()):
    #         self.inventory[class_type][key] = 0
    #
    #     self.inventory[class_type][key] += amount
    #
    #     final = {}
    #     for x in self.inventory.items():
    #         final[x[0]] = dict(sorted(x[1].items()))
    #     self.inventory = final

