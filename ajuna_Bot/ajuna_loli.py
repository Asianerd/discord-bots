import discord
from discord.ext import commands
import random
import pickle
from pathlib import Path

import Events
import Formatting
import Dependencies
import Commands

client = commands.Bot(command_prefix=Dependencies.command_prefix)
Events.init(client)

bot_token = pickle.load(open(f"{Dependencies.save_file_path}/ajuna - Token", "rb"))

Commands.init(client)
Dependencies.initialize()

client.run(bot_token)
