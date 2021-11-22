from enum import Enum
import json
import os


class ItemType(Enum):
    Cookie = 0
    Tea = 1
    billy_os = 2
    PP_yes = 3
    ajian_bat = 4


class Item:
    loot_table = []
    item_data = {}

    def __init__(self, _type):  # Dont use this method; think of it as a private static method
        _item = Item.item_data[str(_type)]

        self.name = _item["name"]
        self.description = _item["description"]

    """Statics"""
    @staticmethod
    def initialize():
        Item.loot_table = []
        Item.item_data = json.load(open("Economy/item_data.json"))


class Inventory:
    def __init__(self):
        self.collection = {}
        for x in ItemType:
            self.collection[x] = 0

    def add(self, item_type, amount=1):
        self.collection[item_type] += amount

    # Name this better as well
    def wording(self):
        if len([x for x in ItemType if self.collection[x] > 0]) <= 0:
            return "No items in your inventory!"
        return "\n".join([f"• `{self.collection[x]}` **{x.name}**" for x in ItemType if self.collection[x] > 0])
