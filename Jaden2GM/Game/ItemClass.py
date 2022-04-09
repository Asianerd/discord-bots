from enum import Enum
import json

from . import StatusEffects
from .StatusEffects import PropertyContainer

# i dont know why a normal import wont work

item_stats = {}
equipment_stats = {}
# Weapon(ItemType) : {key:value}
# Armour(ItemType) : {key:value}
# Accessory(ItemType) : {key:value}


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


class Weapon:
    # TODO : Implement debuff system (for enemies)

    def __init__(self, item_id):
        self_data = equipment_stats[ItemType.weapon][item_id.name]
        self.name = self_data['name']
        self.item_id = item_id

        self.weapon_type = [x for x in Weapon.WeaponType if x.name.lower() == self_data['weapon_type']][0]
        self.elements = [[x for x in Elements if x.name.lower() == i][0] for i in self_data['elements']]
        self.rarity = [x for x in Rarity if x.name.lower() == self_data['rarity']][0]

        self.damage = self_data['damage']
        self.crit_rate = self_data['crit_rate']

        self.stamina_usage = self_data['stamina_usage']
        self.mana_usage = self_data['mana_usage']

        self.buffs = PropertyContainer(self_data['buffs'])

    def as_dict(self):
        final = dict(self.__dict__)
        final['item_id'] = self.item_id.name

        final['weapon_type'] = self.weapon_type.name
        final['elements'] = [x.name for x in self.elements]
        final['rarity'] = self.rarity.name

        final['buffs'] = self.buffs.as_dict()

        return final

    @staticmethod
    def object_from_dict(data_dict):
        final = Weapon(Weapon.get_enum(data_dict['item_id']))
        return final

    @classmethod
    def get_enum(cls, name):
        for x in cls.ItemID:
            if x.name == name:
                return x

    class ItemID(Enum):
        # sword
        dull_blade = 0
        cold_blade = 1
        silver_blade = 2
        dark_iron_blade = 3
        twilight_sword = 4

        # spear
        adventurer_protector = 100
        iron_spear = 101

        # bow
        hunter_bow = 200
        seasoned_hunter_bow = 201

        # glove
        waster_glove = 300
        mercenary_glove = 301

        # codex
        apprentice_note = 400
        handy_grimoire = 401

    class WeaponType(Enum):
        sword = 0
        spear = 1

        bow = 10

        glove = 20

        codex = 30


class Blessing:
    def __init__(self, item_id):
        self_data = equipment_stats[ItemType.blessing][item_id.name]
        self.name = self_data['name']
        self.item_id = item_id

        self.blessing_type = [x for x in Blessing.BlessingType if x.name.lower() == self_data['blessing_type']][0]
        self.elements = [[x for x in Elements if x.name.lower() == i][0] for i in self_data['elements']]
        self.rarity = [x for x in Rarity if x.name.lower() == self_data['rarity']][0]

        self.property_holder = StatusEffects.PropertyContainer(self_data['buffs'])

    def as_dict(self):
        final = dict(self.__dict__)

        final['item_id'] = self.item_id.name
        final['blessing_type'] = self.blessing_type.name
        final['elements'] = [x.name for x in self.elements]

        final['rarity'] = self.rarity.name

        final.pop('property_holder')

        return final

    @staticmethod
    def object_from_dict(data_dict):
        final = Blessing(Blessing.get_enum(data_dict['item_id']))
        return final

    @classmethod
    def get_enum(cls, name):
        for x in cls.ItemID:
            if x.name == name:
                return x

    class ItemID(Enum):
        basic_earring = 0

        iron_bracelet = 100

        enchanted_headband = 200

        amuletum_inexpeditus = 1000

    class BlessingType(Enum):
        earring = 0
        headband = 1

        bracelet = 2


class ItemType(Enum):
    consumable = 0
    equipment = 1

    weapon = 10
    armour = 11
    blessing = 12


class Rarity(Enum):
    Common = 0
    Uncommon = 1
    Rare = 2
    Epic = 3
    Legendary = 4

    Inexpeditus = 10


class Elements(Enum):
    fire = 0
    water = 1
    earth = 2
    wind = 3
    ice = 4
    lightning = 5
    nature = 6

    dark = 7
    light = 8


def initialize():
    global item_stats, equipment_stats
    with open('Data/item_data.json', 'r', encoding='utf-8') as file:
        item_stats = json.load(file)
    with open('Data/equipment_data.json', 'r', encoding='utf-8') as file:
        _data = json.load(file)
        equipment_stats[ItemType.weapon] = _data['weapon']
        equipment_stats[ItemType.blessing] = _data['blessing']
        equipment_stats['item_symbols'] = _data['item_symbols']
        equipment_stats['rarity_colours'] = _data['rarity_colours']
        equipment_stats['type_names'] = _data['type_names']
        equipment_stats['element_symbols'] = _data['element_symbols']
    Consumable.initialize()


def search_item(name):
    for x in Consumable.collection.items():
        if x[1].name.lower() == name:
            return [ItemType.consumable, x[1]]
    for x in equipment_stats[ItemType.weapon].items():
        if x[1]['name'].lower() == name:
            return [ItemType.weapon, x[1]]
    for x in equipment_stats[ItemType.blessing].items():
        if x[1]['name'].lower() == name:
            return [ItemType.blessing, x[1]]
