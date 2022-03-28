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
        for x in self.effects.items():
            x[1] -= 1

        self.effects = dict([x for x in self.effects.items() if x[1] > 0])
        # remove all effects with 0 duration

    def as_dict(self):
        return self.__dict__

    @staticmethod
    def object_from_dict(data_dict):
        final = EffectContainer()
        final.__dict__ = data_dict
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