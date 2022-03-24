from enum import Enum
import enum


class Consumable:
    collection = {}

    item_symbols = {}
    display_names = {}

    def __init__(self, _id, _class, price, description):
        self.item_id = _id
        self.item_class = _class

        self.name = Consumable.display_names[_id]
        self.price = price
        self.description = description

    @classmethod
    def initialize(cls):
        Consumable.item_symbols = {
            Consumable.ItemID.bread: ":bread:",
            Consumable.ItemID.apple: ":apple:",
            Consumable.ItemID.apple_pie: ":pie:",
            Consumable.ItemID.golden_apple: "<:golden_apple:955824833965477908>",

            Consumable.ItemID.ironskin_potion: "<:ironskin_potion:956411586975793162>",
            Consumable.ItemID.wrath_potion: "<:wrath_potion:956412709023399937>",
            Consumable.ItemID.adrenaline_vial: "<:adrenaline_vial:956412708834672671>"
        }

        Consumable.display_names = {
            Consumable.ItemID.bread: "Bread",
            Consumable.ItemID.apple: "Apple",
            Consumable.ItemID.apple_pie: "Apple Pie",
            Consumable.ItemID.golden_apple: "Golden Apple",

            Consumable.ItemID.ironskin_potion: "Ironskin Potion",
            Consumable.ItemID.wrath_potion: "Wrath Potion",
            Consumable.ItemID.adrenaline_vial: "Adrenaline Vial"
        }

        cls.collection[Consumable.ItemID.bread] = Consumable(Consumable.ItemID.bread, Consumable.ItemClass.food, 5, "Prevents hunger for 3 rounds\nCrunchy and tasty...")
        cls.collection[Consumable.ItemID.apple] = Consumable(Consumable.ItemID.apple, Consumable.ItemClass.food, 10, "Prevents hunger for 4 rounds\nA juicy and sweet red apple.")
        cls.collection[Consumable.ItemID.apple_pie] = Consumable(Consumable.ItemID.apple_pie, Consumable.ItemClass.food, 25, "Prevents hunger for 6 rounds\nSmoking hot and smell delicious...")
        cls.collection[Consumable.ItemID.golden_apple] = Consumable(Consumable.ItemID.golden_apple, Consumable.ItemClass.food, 50, "Prevents hunger for 10 rounds\nIt's shine enchants you...")

        cls.collection[Consumable.ItemID.ironskin_potion] = Consumable(Consumable.ItemID.ironskin_potion, Consumable.ItemClass.potion, 20, "Increases defence by 10\nHard to swallow.")
        cls.collection[Consumable.ItemID.wrath_potion] = Consumable(Consumable.ItemID.wrath_potion, Consumable.ItemClass.potion, 20, "Increase damage by 10%\nBitter, like anger.")
        cls.collection[Consumable.ItemID.adrenaline_vial] = Consumable(Consumable.ItemID.adrenaline_vial, Consumable.ItemClass.potion, 50, "Increase damage by 25% and reduce defense by 10%\nHolding this in your hand makes you feel powerful...")

    def readable(self):
        return f"{Consumable.item_symbols[self.item_id]} **{self.name}**   - ${self.price}\n" \
               f"*{self.description}*\n"

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
    Consumable.initialize()
    Equipment.initialize()


def all_collections():
    return list(Consumable.collection.values()) + list(Equipment.collection.values())
