from enum import Enum
import json
from . import StatusEffects
# i dont know why a normal import wont work

item_stats = {}


class Consumable:
    collection = {}

    item_symbols = {}
    display_names = {}

    consumable_stats = {}

    def __init__(self, _id, _class):
        self.item_id = _id
        self.item_class = _class

        data_table = item_stats['consumable'][self.item_id.name]

        self.name = Consumable.display_names[_id]
        self.price = data_table['price']
        self.description = data_table['description']

        self.effects = {}
        for x in dict(data_table['effects']).items():
            self.effects[StatusEffects.get_enum(x[0])] = x[1]
        # effect enum : duration
        self.health_return = data_table['health_return']  # how much health is gained from using this

    @classmethod
    def initialize(cls):
        Consumable.item_symbols = {
            Consumable.ItemID.bread: ":bread:",
            Consumable.ItemID.apple: ":apple:",
            Consumable.ItemID.apple_pie: ":pie:",
            Consumable.ItemID.golden_apple: "<:golden_apple:955824833965477908>",

            Consumable.ItemID.ironskin_potion: "<:ironskin_potion:956411586975793162>",
            Consumable.ItemID.wrath_potion: "<:wrath_potion:956412709023399937>",
            Consumable.ItemID.adrenaline_vial: "<:adrenaline_vial:956412708834672671>",
        }

        Consumable.display_names = {
            Consumable.ItemID.bread: "Bread",
            Consumable.ItemID.apple: "Apple",
            Consumable.ItemID.apple_pie: "Apple Pie",
            Consumable.ItemID.golden_apple: "Golden Apple",

            Consumable.ItemID.ironskin_potion: "Ironskin Potion",
            Consumable.ItemID.wrath_potion: "Wrath Potion",
            Consumable.ItemID.adrenaline_vial: "Adrenaline Vial",
        }

        for x in Consumable.ItemID:
            cls.collection[x] = Consumable(x, [Consumable.ItemClass.food, Consumable.ItemClass.potion][x in [
                Consumable.ItemID.ironskin_potion,
                Consumable.ItemID.wrath_potion,
                Consumable.ItemID.adrenaline_vial
            ]])

    def readable(self):
        newline = '\n'
        return f"{Consumable.item_symbols[self.item_id]} **{self.name}**   - ${self.price}\n" \
               f"*{self.description}*\n" \
               f"{('`Health : ' + str(self.health_return) + '`' + newline if (self.health_return != 0) else '')}" + (f"Effects : **{', '.join([StatusEffects.EffectContainer.display_names[x[0]] for x in self.effects.items()])}**" if self.effects else '') + "\n"

    @classmethod
    def get_enum(cls, name):
        for x in cls.ItemID:
            if x.name == name:
                return x

    class ItemID(Enum):
        bread = 0
        apple = 1
        golden_apple = 2
        apple_pie = 3

        ironskin_potion = 50
        wrath_potion = 51
        adrenaline_vial = 52

    class ItemClass(Enum):
        food = 0
        potion = 1


class Equipment:
    collection = {

    }

    def __init__(self, _id, _class, name, price, description):
        self.item_id = _id
        self.item_class = _class

        self.name = name
        self.price = price
        self.description = description

    @classmethod
    def initialize(cls):
        cls.collection[Equipment.ItemID.iron_shortsword] = Equipment(Equipment.ItemID.iron_shortsword, Equipment.ItemClass.weapon, "Iron Shortsword", 50, "It's pretty dull, but it does it's job")
        cls.collection[Equipment.ItemID.platinum_shortsword] = Equipment(Equipment.ItemID.platinum_shortsword, Equipment.ItemClass.weapon, "Platinum Shortsword", 50, "A bit heavy and hard to swing but deals a strong blow")

    @classmethod
    def get_enum(cls, name):
        for x in cls.ItemID:
            if x.name == name:
                return x

    class ItemID(Enum):
        iron_shortsword = 0
        platinum_shortsword = 1

    class ItemClass(Enum):
        weapon = 0
        armour = 1
        accessory = 2


class ItemType(Enum):
    consumable = 0
    equipment = 1


def initialize():
    global item_stats
    with open('Data/item_data.json', 'r', encoding='utf-8') as file:
        item_stats = json.load(file)
    Consumable.initialize()
    Equipment.initialize()


def all_collections():
    return list(Consumable.collection.values()) + list(Equipment.collection.values())
