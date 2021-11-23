class Experience:
    def __init__(self):
        self.level = 0

        self.current = 0
        self.next_level_requirement = 0
        self.calculate_next_requirement()

        self.total = 0

    def calculate_next_requirement(self):
        self.next_level_requirement = (2 ** self.level) * 10
