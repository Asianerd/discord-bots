from discord.ext import commands

import Dependencies
import Events
import Quest
import User

import ShopModule

# be really careful with the imports; dont wanna cause a circular import
from Game import StatusEffects
import BattleModule

# So basically, the bot is about quest system & basic conversation
"""
Name : Jaden2GM

Quest system // Done
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

StatusEffects.EffectContainer.initialize()

Events.init(client)
ShopModule.init(client)
BattleModule.init(client)


client.run(Dependencies.token)
