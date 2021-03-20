import discord
from discord.ext import commands
import time
import pickle
import random
from pathlib import Path

client = commands.Bot(command_prefix='!')
saveFilePath = Path(".")/"RollerViking_Data"
botToken = pickle.load(open(f"{saveFilePath}/RollerVikings - Token","rb"))

"""Class definitions"""


class Suggestion:
    def __init__(self, _suggestion, _time, _user):
        self.suggestion = _suggestion
        self.time = _time
        self.user = _user


try:
    suggestions = pickle.load(open(f'{saveFilePath}/RollerVikings - Suggestions', 'rb'))
except FileNotFoundError:
    pickle.dump(suggestions := [], open(f'{saveFilePath}/RollerVikings - Suggestions', 'wb'))

"""Functions"""


def saveSuggestions():
    pickle.dump(suggestions, open(f'{saveFilePath}/RollerVikings - Suggestions', 'wb'))


def RandomColour():
    return random.randint(1048576, 0xFFFFFF)


"""Commands"""


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("RollerVikings"))
    print('Bot is ready')


@client.command(pass_context=True, brief='Use this to submit suggestions. Please keep it concise and short')
async def suggest(ctx, *args):
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
                              f'{index+1}. [{time.strftime("%d/%m/%y", x.time)}] {x.user} - {x.suggestion}'
                              for index,x in enumerate(suggestions)
                          ]), colour=RandomColour())
    await ctx.send(embed=final)

@client.command()
async def remove_suggestion(ctx,args):
    try:
        index = int(args)
        if (index >= 1) and (index <= (len(suggestions))):
            suggestions.pop(index-1)
            await ctx.send("Suggestion successfully removed.")
        else:
            await ctx.send("Index not in range.")
    except ValueError:
        await ctx.send("Parameter was not an integer.")
    saveSuggestions()

client.run(botToken)
