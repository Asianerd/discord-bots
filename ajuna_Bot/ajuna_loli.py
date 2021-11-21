import discord
from discord.ext import commands
import random
import pickle
from pathlib import Path

import Events
import Formatting
import Dependencies
import Commands
from Economy import Economy
from Economy import Item

client = commands.Bot(command_prefix=Dependencies.command_prefix)
Events.init(client)
"""
discord-bots
    - <dir> ajuna_Data
    - <dir> ajuna_loli
"""
bot_token = pickle.load(open(f"{Dependencies.save_file_path}/ajuna - Token", "rb"))

Commands.init(client)
Economy.init(client)
Item.Item.initialize()

client.run(bot_token)
