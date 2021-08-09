from pathlib import Path
import pickle

command_prefix = "\\"
author_id = 517998886141558786
save_file_path = Path(".") / "ajian_Data"
send_messages = False
unsendable_content = ['pinceapple', f'{command_prefix}toggle']
emojis = []
disposable_messages = []

reactions = ["\N{WASTEBASKET}"]


def save():
    #pickle.dump(emojis, open(f"{save_file_path}/asian - Emojis", "wb"))
    pass


def load():
    global emojis
    try:
        #return pickle.load(open(f"{save_file_path}/asian - Emojis", "rb"))
        pass
    except FileNotFoundError:
        emojis = []
        save()
        return emojis
