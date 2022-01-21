import discord
from discord.ext import commands

import Dependencies
import Events
import Quest
import User

# So basically, the bot is about quest system & basic conversation
"""
Name : Jaden2GM

Quest system
    - Based on other games
    - Manual checking if someone completes the quest

Basic conversation // Done
    - Alexa API
"""

Dependencies.init()
User.User.initialize()
Quest.Quest.initialize()

client = commands.Bot(
    command_prefix=Dependencies.command_prefix,
    help_command=None
)

Events.init(client)

client.run(Dependencies.token)
