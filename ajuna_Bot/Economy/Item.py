from enum import Enum


class Item:
    loot_table = []

    class ItemType(Enum):
        Cookie = 0
        Tea = 1
        billy_os = 2
        PP_yes = 3
        ajian_bat = 4

    def __init__(self):
        pass

    """Statics"""
    @staticmethod
    def initialize():
        Item.loot_table = []


class Inventory:
    def __init__(self):
        self.collection = {}
        for x in Item.ItemType:
            self.collection[x] = 0

    def add(self, item_type, amount=1):
        self.collection[item_type] += amount

    # Name this better as well
    def wording(self):
        if len([x for x in Item.ItemType if self.collection[x] > 0]) <= 0:
            return "No items in your inventory!"
        return "\n".join([f"• `{self.collection[x]}` **{x.name}**" for x in Item.ItemType if self.collection[x] > 0])
