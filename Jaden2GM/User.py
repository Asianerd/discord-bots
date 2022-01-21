import json
import time

import Quest


class User:
    users = []

    @staticmethod
    def initialize():
        User.users = []
        User.load()

    @staticmethod
    def save():
        final = {}
        for x in User.users:
            final[str(x.user_id)] = x.__dict__
        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump(final, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load():
        User.users = []
        with open('users.json', 'r') as file:
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

        User.users.append(self)

    def update_name(self, name):
        self.username = str(name[0:32])
        User.save()

    def quests_completed(self):
        return len([x for x in Quest.Quest.quests if self.user_id in x.users_completed])

    def daily_points(self):
        if (int(time.time()) - self.last_daily_points) >= 86400:
            self.points += 5
            self.last_daily_points = int(time.time())
            return True
        return False
