import sys
import discord
sys.path.append("..")
import Formatting


class Experience:
    def __init__(self, level=0, current=0, total=0):
        self.level = level

        self.current = current
        self.next_level_requirement = 0
        self.calculate_next_requirement()

        self.total = total

    def calculate_next_requirement(self):
        self.next_level_requirement = (2 ** self.level) * 10

    async def add_exp(self, ctx, amount):
        self.current += amount
        self.total += amount
        if self.current >= self.next_level_requirement:
            self.current -= self.next_level_requirement

            self.level += 1
            self.calculate_next_requirement()
            await (await ctx.send(embed=discord.Embed(
                title=f"Level up!  {self.level - 1} -> {self.level}",
                color=Formatting.colour()
            ))).delete(delay=3)