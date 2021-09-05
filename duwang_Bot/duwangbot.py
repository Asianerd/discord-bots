import discord
from discord.ext import commands
import pickle

token_file_path = "duwangbot - Token"

token = pickle.load(open(token_file_path, 'rb'))
powered = [517998886141558786, 654141711236333579]
owner_id = 654141711236333579
toggled = False

prefix = ">"
client = commands.Bot(command_prefix=prefix)


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


async def delayed_delete(message, delay=3):
    await message.delete(delay=delay)


def find_in_message(content, target):
    info = ""
    for x in content:
        if x[0:len(target)] == target:
            info = x[len(target) + 1:]
    return info


@client.event
async def on_ready():
    print("Duwangbot is ready!")


@client.command()
async def toggle(ctx):
    global toggled
    try:
        await ctx.message.delete()
    except:
        pass
    if ctx.message.author.id in powered:
        toggled = not toggled


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == f"{prefix}toggle":
        await message.delete()

    if message.author.id == owner_id:
        if toggled and (message.content[0] != prefix):
            await message.delete()
            await message.channel.send(message.content)
    await client.process_commands(message)

@client.command()
async def change_pres(ctx, *args):
    await ctx.message.delete()
    acts = ['g', 'l', 's', 'w']
    wanted_act = args[0]
    wanted_subject = args[1]
    if wanted_act == acts[2]:
        if len(args) >= 3:
            wanted_link = args[2]
        else:
            final = "Arguments insufficient or incorrect  - Streaming status needs to be provided with a url"
            await delayed_delete(await ctx.send(final))
            return
    else:
        wanted_link = ''
    if wanted_act in acts:
        if wanted_act == acts[0]:
            await client.change_presence(activity=discord.Game(name=wanted_subject))
            final = f'Activity set to **Playing {wanted_subject}**'
        elif wanted_act == acts[1]:
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening, name=wanted_subject))
            final = f'Activity set to **Listening to {wanted_subject}**'
        elif wanted_act == acts[2]:
            await client.change_presence(activity=discord.Streaming(name=wanted_subject, url=wanted_link))
            final = f'Activity set to **Streaming {wanted_subject} at {wanted_link}**'
        else:
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=wanted_subject))
            final = f'Activity set to **Watching {wanted_subject}**'
    else:
        final = f'Arguments insufficient or incorrect   -{args, wanted_act, wanted_subject}'
    await delayed_delete(await ctx.send(final))

@client.command()
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send(embed=discord.Embed(
        title=f"**Ping :** `{int(client.latency * 1000)}`",
        color=int((int(get_ping_colour(int(client.latency * 1000))[0])) + (
                int(get_ping_colour(int(client.latency * 1000))[1]) * 256))
    ))

@client.command(hidden=True)
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


client.run(token)
