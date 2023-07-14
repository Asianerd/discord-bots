import discord
import json
import time
import random
import asyncio

from discord.ext import tasks, commands

import Dependencies


def init(bot: discord.Bot):
    @bot.event
    async def on_ready():
        print(f"{bot.user} is awake!")

    @bot.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return
        if reaction.message in Dependencies.disposable_messages:
            await reaction.message.delete()
