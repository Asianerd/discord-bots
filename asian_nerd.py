import discord
from discord.ext import commands
from discord.ext.commands import has_role
import random
import pickle
from pathlib import Path

client = commands.Bot(command_prefix='\\')

author_id = 517998886141558786
saveFilePath = Path(".") / "asian_Data"
BotToken = pickle.load(open(f"{saveFilePath}/asian - Token", "rb"))
SendMessages = False
disallowed_messages = ["pinceapple",f"{client.command_prefix}toggle"]
emojis = []

# Functions
def random_colour():
    return random.randint(0x100000, 0xFFFFFF)


def get_ping_colour(_i):
    _min = 0
    _max = 500
    _percent = (_i - _min) / _max - _min
    _r = 510 * _percent
    _g = 510 * (1 - _percent)
    if _r > 255:
        _r = 255
    if _g > 255:
        _g = 255
    return _r, _g


def save():
    pickle.dump(emojis, open(f"{saveFilePath}/asian - Emojis", "wb"))


def load():
    global emojis
    try:
        emojis = pickle.load(open(f"{saveFilePath}/asian - Emojis", "rb"))
    except FileNotFoundError:
        emojis = []
        save()


#

@client.event
async def on_ready():
    load()
    print("Bot ready")


@client.command(pass_context=True, brief="Changes the bot's status",
                description="Changes the bot description.\nFormat:\ng - Game\nl - Listening\ns - Streaming\nw - Watching")
async def change_pres(ctx, *args):
    acts = ['g', 'l', 's', 'w']
    wanted_act = args[0]
    wanted_subject = args[1]
    if wanted_act == acts[2]:
        if len(args) >= 3:
            wanted_link = args[2]
        else:
            wanted_link = ''
            await ctx.send(f'Arguments insufficient or incorrect  - Streaming status needs to be provided with a url')
    else:
        wanted_link = ''
    if wanted_act in acts:
        if wanted_act == acts[0]:
            await client.change_presence(activity=discord.Game(name=wanted_subject))
            await ctx.send(f'Activity set to **Playing {wanted_subject}**')
        elif wanted_act == acts[1]:
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening, name=wanted_subject))
            await ctx.send(f'Activity set to **Listening to {wanted_subject}**')
        elif wanted_act == acts[2]:
            await client.change_presence(activity=discord.Streaming(name=wanted_subject, url=wanted_link))
            await ctx.send(f'Activity set to **Streaming {wanted_subject} at {wanted_link}**')
        elif wanted_act == acts[3]:
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=wanted_subject))
            await ctx.send(f'Activity set to **Watching {wanted_subject}**')
    else:
        await ctx.send(f'Arguments insufficient or incorrect   -{args, wanted_act, wanted_subject}')


@client.command()
async def ping(ctx): await ctx.send(f'`Ping : {int(client.latency * 1000)}ms`')


@client.command(pass_context=True, hidden=True)
@has_role('Bot Doctor')
async def change_stat(ctx, args):
    if args in ['do', 'on', 'id', 'in']:
        if args == 'do':
            await client.change_presence(status=discord.Status.do_not_disturb)
        if args == 'on':
            await client.change_presence(status=discord.Status.online)
        if args == 'id':
            await client.change_presence(status=discord.Status.idle)
        if args == 'in':
            await client.change_presence(status=discord.Status.invisible)
    else:
        await ctx.send('arg not in activity list')


@client.command()
async def join_me(ctx, args):
    await discord.VoiceChannel.connect(await client.fetch_channel(args), reconnect=True)


@client.command()
async def toggle(ctx):
    global SendMessages
    if ctx.message.author.id == author_id: SendMessages = not SendMessages


@client.event
async def on_message(message):
    if ('pinceapple' not in message.content) and SendMessages:
        if message.author.id == author_id:
            await message.delete()
            await message.channel.send(message.content)
    await client.process_commands(message)


@client.command()
async def fetch_pfp(ctx):
    if not ctx.message.mentions:
        selected_user = ctx.message.author
    else:
        selected_user = ctx.message.mentions[0]
    pfp = selected_user.avatar_url
    embed = discord.Embed(title=f"**{selected_user.name}'s profile picture**",
                          color=random_colour())
    embed.set_image(url=pfp)
    await ctx.send(embed=embed)


@client.command()
async def fetch_emojis(ctx):
    [emojis.append(x) for x in ctx.message.guild.emojis]
    await ctx.send("Gathering done")


@client.command()
async def fetch_emoji_list(ctx,args="0"):
    try:
        index_wanted = int(args) - 1
    except ValueError:
        index_wanted = 0

    _emojis = [" | ".join([f"`{i.name} :`{str(i)}" for i in x]) for x in [emojis[x:x + 37] for x in range(0, len(emojis), 37)]]

    if index_wanted not in range(0, len(_emojis)):
        finalEmbed = discord.Embed(
            title="Index out of range.",
            description=f"Please select a number between 1 and {len(_emojis)}",
            colour=random_colour()
        )
    else:
        finalEmbed = discord.Embed(
            title="**Emojis**",
            description=_emojis[index_wanted],
            colour=random_colour()
        )

    await ctx.send(embed=finalEmbed)

@client.command()
async def send_emoji(ctx, args):
    try:
        index_wanted = int(args)-1
    except ValueError:
        index_wanted = -1
    


    if (index_wanted not in range(0,len(emojis))) or (index_wanted==-1):
        await ctx.send(embed=discord.Embed(
            title="Index out of range.",
            description=f"Please select a number between 1 and {len(emojis)}",
            colour=random_colour()
        ))
    else:
        await ctx.send(emojis[index_wanted])




client.run(BotToken)
