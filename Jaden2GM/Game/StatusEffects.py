from enum import Enum


class EffectContainer:
    # this object is on every user
    #   - holds all effect objects and etc etc
    display_names = {}

    @staticmethod
    def initialize():
        EffectContainer.display_names = {
            Effects.ironskin: "Ironskin",
            Effects.wrath: "Wrath",
            Effects.adrenaline: "Adrenaline",
            Effects.regeneration: "Regeneration"
        }

    def __init__(self):
        self.effects = {

        }
        # Effects(Enum) : duration(int)

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
        return final

    @staticmethod
    def object_from_dict(data_dict):
        final = EffectContainer()
        final.__dict__ = data_dict
        _effects = {}
        for x in data_dict['effects'].items():
            _effects[get_enum(x[0])] = x[1]
        final.effects = dict(_effects)
        return final


def get_enum(string):
    for x in Effects:
        if x.name == string:
            return x


class Effects(Enum):
    ironskin = 0
    wrath = 1
    adrenaline = 2
    regeneration = 3