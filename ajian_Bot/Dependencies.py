from pathlib import Path
import pickle

command_prefix = "\\"
author_id = 517998886141558786
save_file_path = Path("..") / "asian_Data"
send_messages = False
unsendable_content = ['pinceapple', f'{command_prefix}toggle']
emojis = []
disposable_messages = []

reactions = ["\N{WASTEBASKET}"]


def save(emojis):
    pickle.dump(emojis, open(f"{save_file_path}/asian - Emojis", "wb"))


def load():
    try:
        return pickle.load(open(f"{save_file_path}/asian - Emojis", "rb"))
    except FileNotFoundError:
        return []
