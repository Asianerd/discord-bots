import json
import User


class Quest:
    """"""
    """
    name
    description
    reward
    
    time range
    
    if is ongoing
    """

    quests = []

    @staticmethod
    def initialize():
        Quest.quests = []
        Quest.load()

    @staticmethod
    def save():
        final = {}
        for x in Quest.quests:
            object_dictionary = x.__dict__
            final[str(x.id)] = object_dictionary
        with open('quest.json', 'w', encoding='utf-8') as file:
            json.dump(final, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load():
        Quest.quests = []
        with open('quest.json', 'r') as file:
            data_file: dict = json.load(file)
            for x in data_file.items():
                data = x[1]

                item = Quest('', '', '', 0)
                item.__dict__ = data

    @staticmethod
    def complete_quest(user_id, quest_id):
        if quest_id in [x.id for x in Quest.quests]:
            target_quest = [x for x in Quest.quests if x.id == quest_id][0]
            result = target_quest.add_completed_user(user_id)
            return {
                True: [True, "User completed quest successfully"],
                False: [False, "User has already completed this quest"]
            }[result]
        else:
            return False, f"Invalid quest id; current quest-ids : [{', '.join([str(x.id) for x in Quest.quests])}]"

    @staticmethod
    def fetch_split_quests(page, amount=6):
        split_quests = [[]]
        for index, item in enumerate(Quest.quests):
            if ((index % amount) == 0) and (index != 0):
                split_quests.append([])

            split_quests[-1].append(item)
        return split_quests[page]

    def __init__(self, name, description, rewards, points):
        self.name = name
        self.description = description
        if len(Quest.quests) != 0:
            self.id = sorted([x.id for x in Quest.quests])[-1] + 1
        else:
            self.id = len(Quest.quests) + 1

        self.rewards = rewards
        self.points = points

        self.users_completed = []

        self.is_ongoing = True

        Quest.quests.append(self)

    def get_info(self):
        return f"`{str(self.id).rjust(2, '0')}`| **{self.name}**\n" \
               f" - {self.description[:150]+'...' if (len(self.description) >= 150) else self.description}\n"

    def add_completed_user(self, user_id):
        if not (user_id in self.users_completed):
            self.users_completed.append(user_id)
            [x for x in User.User.users if x.user_id == user_id][0].points += self.points
            return True
        return False
