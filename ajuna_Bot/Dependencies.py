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
english_words = {}


class ReactionType(Enum):
    wastebasket = 0


reactions = {
    ReactionType.wastebasket: "\N{WASTEBASKET}",
}


async def delayed_delete(message, delay=3):
    await message.delete(delay=delay)


async def dispose_message(ctx):
    disposable_messages.append(ctx)
    await ctx.add_reaction(reactions[ReactionType.wastebasket])


def initialize():
    global english_words
    with open("english_words.txt") as word_file:  # Proudly plucked from SO
        english_words = set(word.strip().lower() for word in word_file)


def is_valid_english(word):
    return word in english_words
