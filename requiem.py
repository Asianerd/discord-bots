import discord
from discord.ext import commands
import pickle

botToken = pickle.load(open("Requiem 2.0 - Token","rb"))

client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print("Bot is ready\n")

@client.command()
async def test(ctx):
    await ctx.send("`[sample text]`")

client.run(botToken)
