import discord
from discord.ext import commands
import random
import pickle
from pathlib import Path

import Events
import Data
import Command

client = commands.Bot(command_prefix=Data.command_prefix)
bot_token = pickle.load(open(f"{Data.save_file_path}/Requiem - Token", "rb"))

Events.init(client)
Command.init(client)

client.run(bot_token)
