class GameValue:
    def __init__(self, min, max, regen, starting_percent=1):
        self.min = min
        self.max = max
        self.regeneration = regen

        self.current = int((self.max - self.min) * starting_percent)

    def regenerate(self, rate=1):
        amount = self.regeneration * rate
        if self.current < self.max:
            self.current += amount
            if self.current > self.max:
                self.current = self.max

    def affect_amount(self, amount):
        self.current += amount

    def affect_percent(self, percent):
        self.current = int((self.max - self.min) * percent)

    def percent(self):
        return self.current / (self.max - self.min)

    def as_dict(self):
        return self.__dict__

    @staticmethod
    def object_from_dict(data_dict):
        final = GameValue(0, 0, 0)
        final.__dict__ = data_dict
        return final
