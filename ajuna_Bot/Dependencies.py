from pathlib import Path
import pickle
from enum import Enum

command_prefix = "\\"
author_id = 517998886141558786
save_file_path = Path(".") / "ajuna_Data"
send_messages = False
unsendable_content = ['pinceapple', f'{command_prefix}toggle']
authorized_users = [517998886141558786, 859005581414236160]
emojis = []
disposable_messages = []


class ReactionType(Enum):
    wastebasket = 0
    no1 = 1
    no2 = 2
    no3 = 3
    no4 = 4
    no5 = 5


reactions = {
    ReactionType.wastebasket: "\N{WASTEBASKET}",
}


async def delayed_delete(message, delay=3):
    await message.delete(delay=delay)


async def dispose_message(ctx):
    disposable_messages.append(ctx)
    await ctx.add_reaction(reactions[ReactionType.wastebasket])
