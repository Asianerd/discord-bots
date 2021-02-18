import discord
from discord.ext import commands
import time
import pickle
import random

client = commands.Bot(command_prefix='!')

"""Class definitions"""

class Suggestion:
    def __init__(self,_suggestion,_time,_user):
        self.suggestion = _suggestion
        self.time = _time
        self.user = _user

try:
    suggestions = pickle.load(open('RollerVikings - Suggestions','rb'))
except FileNotFoundError:
    pickle.dump(suggestions:=[],open('RollerVikings - Suggestions','wb'))

"""Functions"""

def saveSuggestions():
    pickle.dump(suggestions,open('RollerVikings - Suggestions','wb'))

def RandomColour():
    return random.randint(1048576,0xFFFFFF)

"""Commands"""

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("RollerVikings"))
    print('Bot is ready')

@client.command(pass_context=True,brief='Use this to submit suggestions. Please keep it concise and short')
async def suggest(ctx,*args):
    if not ' '.join(args) == '':
        _user = await client.fetch_user(ctx.message.author.id)
        suggestions.append(Suggestion(' '.join(args),
                                      time.localtime(),
                                      f'{_user.name}#{_user.discriminator}'))
        saveSuggestions()
        await ctx.send(f"Your suggestion, {' '.join(args)}, has been recorded.")
    else:
        await ctx.send("Your suggestion was empty and thus rejected.")

@client.command()
async def get_suggestions(ctx):
    final = discord.Embed(title='***Suggestions***',
                          description='\n'.join([
                              f'[{time.strftime("%d/%m/%y",x.time)}] {x.user} - {x.suggestion}'
                              for x in suggestions
                          ]),colour=RandomColour())
    await ctx.send(embed=final)

@client.command(pass_context=True)
async def get_user(ctx):
    user = await client.fetch_user(ctx.message.author.id)
    await ctx.send(user)

client.run('ODAzODk4NjQ4MzIzOTQ4NTY0.YBEe9Q.38GDvOzgigQT6v5MEZVekeBMWNc')
