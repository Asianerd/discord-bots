from enum import Enum
import json


class EffectContainer:
    # this object is on every user
    #   - holds all effect objects and etc etc
    display_names = {}

    effect_properties = {}

    @staticmethod
    def initialize():
        EffectContainer.display_names = {
            Effects.ironskin: "Ironskin",
            Effects.wrath: "Wrath",
            Effects.adrenaline: "Adrenaline",
            Effects.regeneration: "Regeneration",
            Effects.manic: "Manic",
            Effects.flexible: "Flexible",

            Effects.inexpeditus_inactus: "Inexpeditus Inactus",
            Effects.inexpeditus_invictus: "Inexpeditus Invictus"
        }

        final = {}
        with open('Data/effect_data.json', 'r', encoding='utf-8') as file:
            _data = json.load(file)
            for x in _data.items():
                final[get_enum(x[0])] = PropertyContainer(x[1])
        EffectContainer.effect_properties = final

    def __init__(self):
        self.effects = {

        }
        # Effects(Enum) : duration(int)

        self.property_container = PropertyContainer({})

    def calculate_combination(self, profile):
        properties = []
        for x in profile.equipped_blessings:
            properties.append(x.property_holder)
        for x in self.effects:
            properties.append(EffectContainer.effect_properties[x])
        self.property_container = PropertyContainer.combine_all(properties)

    def update(self):
        for x in self.effects:
            # "why not just loop through item, then x[1] -= 1?" because its x is treated as an immutable tuple
            self.effects[x] -= 1

        self.effects = dict([x for x in self.effects.items() if x[1] > 0])
        # remove all effects with 0 duration

    def as_dict(self):
        final = dict(self.__dict__)
        _effects = {}
        for x in final['effects'].items():
            _effects[x[0].name] = x[1]
        final['effects'] = _effects
        final.pop('property_container')
        return final

    @staticmethod
    def object_from_dict(data_dict):
        final = EffectContainer()
        final.__dict__ = data_dict
        final.property_container = PropertyContainer({})
        _effects = {}
        for x in data_dict['effects'].items():
            _effects[get_enum(x[0])] = x[1]
        final.effects = dict(_effects)
        return final


class PropertyContainer:
    display_names = {
        "max_health": "Max Health",
        "health_regen": "Health Regen",

        "max_stamina": "Max Stamina",
        "stamina_regen": "Stamina Regen",

        "max_mana": "Max Mana",
        "mana_regen": "Mana Regen",

        "damage": "Damage",

        "dodge_chance": "Dodge Chance",

        "crit_chance": "Crit Rate",
        "crit_multiplier": "Crit Damage",

        "defense": "Defense"
    }

    def __init__(self, data_dict):
        self.max_health = 1.0
        self.health_regen = 1.0

        self.max_stamina = 1.0
        self.stamina_regen = 1.0

        self.max_mana = 1.0
        self.mana_regen = 1.0

        self.damage = 1.0

        self.dodge_chance = 1.0

        self.crit_chance = 1.0
        self.crit_multiplier = 1.0
        # ^ basically crit damage

        self.defense = 1.0

        self.assign_from_dict(data_dict)

    @staticmethod
    def combine_all(properties):
        # combine from blessings and status effects
        final = PropertyContainer({})
        for x in properties:
            for d in x.__dict__.items():
                final.__dict__[d[0]] += (d[1] - 1)
        return final

    def assign_from_dict(self, data_dict):
        for x in data_dict.items():
            if x[0] in self.__dict__:
                self.__dict__[x[0]] = x[1]

    def as_dict(self):
        return dict([x for x in self.__dict__.items() if x[1] != 1.0])


def get_enum(string):
    for x in Effects:
        if x.name == string:
            return x


class Effects(Enum):
    ironskin = 0

    wrath = 100
    adrenaline = 101

    regeneration = 300
    manic = 301

    flexible = 400

    inexpeditus_inactus = 10000
    inexpeditus_invictus = 10001
