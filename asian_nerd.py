import discord
from discord.ext import commands
from discord.ext.commands import has_role
import random
import pickle
from pathlib import Path

client = commands.Bot(command_prefix='\\')

saveFilePath = Path(".") / "asian_Data"
BotToken = pickle.load(open(f"{saveFilePath}/asian - Token", "rb"))
SendMessages = False
emojis = []


class Emoji:
    def __init__(self, name, _id):
        self.name = name
        self.id = _id

    def get_emoji(self):
        return f"<:{self.name}:{self.id}>"


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
    if ctx.message.author.id == 517998886141558786: SendMessages = not SendMessages


@client.event
async def on_message(message):
    if ('pinceapple' not in message.content) and SendMessages:
        if message.author.id == 517998886141558786:
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
async def send_emoji(ctx, args):
    try:
        index = int(args)

        if (index >= 0) and (index <= (len(emojis) - 1)):
            await ctx.send(emojis[index].get_emoji())
            return
        else:
            message = await ctx.send("`Index does not fit the list.`")

    except ValueError:
        message = await ctx.send("`Index is not an integer.`")
    await message.delete(delay=3)


@client.command()
async def get_emojis(ctx, args="none"):
    if args == "none":
        await ctx.send(embed=discord.Embed(
            title="**`Emojis`**",
            description=(
                "\n".join([f"`{str(i).rjust(2, ' ')}.` {x.get_emoji()} `{x.name}`" for i, x in enumerate(emojis)]))))
    else:
        await ctx.send(embed=discord.Embed(
            title="**`Emojis`**",
            description=("\n".join(
                [f"`{str(i).rjust(2, ' ')}.` {x.get_emoji()} `{x.name} {x.id}`" for i, x in enumerate(emojis)]))))


@client.command()
async def upload_emoji(ctx, args):
    if ctx.message.author.id == 517998886141558786:
        try:
            _name = args[2:-1].split(":")[0]
            _id = args[2:-1].split(":")[1]
            emojis.append(Emoji(_name, _id))
            await ctx.send(f"`Emoji uploaded.`<:{_name}:{_id}>` at index {len(emojis) - 1}`")
            return
        except IndexError:
            message = await ctx.send("Unable to upload that emoji.")
    else:
        message = await ctx.send("`You aren't `<@517998886141558786>`, you don't have permission to use this command.`")
    await message.delete(delay=3)
    save()


@client.command()
async def remove_emoji(ctx, args="none"):
    if ctx.message.author.id == 517998886141558786:
        if args != "none":
            try:
                index_wanted = int(args)
                try:
                    wanted_emoji = emojis[index_wanted]
                    emojis.remove(wanted_emoji)
                    await ctx.send(f"{wanted_emoji.get_emoji()}`has been removed from the list.`")
                    return
                except IndexError:
                    message = await ctx.send("`Index out of range.`")
            except ValueError:
                message = await ctx.send("`Parameter is not an int.`")
        else:
            message = await ctx.send("`Parameter not given.`")
    else:
        message = await ctx.send("`You aren't `<@517998886141558786>`, you don't have permission to use this command.`")
    await message.delete(delay=3)
    save()


client.run(BotToken)
