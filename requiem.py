import discord
from discord.ext import commands
from discord.ext.commands import has_role, has_permissions
import random
import pickle

botToken = pickle.load(open("Requiem 2.0 - Token", "rb"))
client = commands.Bot(command_prefix=".")


# Classes
class Exp:
    def __init__(self, _userID):
        self.userId = _userID
        self.username = ''
        self.totalExp = 0
        self.level = 0
        self.currentExp = 0
        self.levelUpRequiredXp = 100

        self.lastSentMessage = ""

    def AddExp(self, msg_content):
        if msg_content != self.lastSentMessage:
            self.lastSentMessage = msg_content
            added_exp = int(len(msg_content) * 2)
            if added_exp > 500:
                added_exp = 500
            self.currentExp += added_exp
            self.totalExp += added_exp

    def CanLevelUp(self):
        return self.currentExp >= self.levelUpRequiredXp

    def LevelUp(self):
        self.level += 1
        self.currentExp -= self.levelUpRequiredXp
        self.levelUpRequiredXp *= 2

    async def SendLevelUp(self, ctx):
        await ctx.send(embed=discord.Embed(title=f"<@{self.userId}> has leveled up!",
                                           description=f"{self.level - 1} --> {self.level}"))

    async def UpdateName(self):
        _name = await client.fetch_user(self.userId)
        self.username = f"{_name.name}#{_name.discriminator}"
#

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


def add_to_log():
    pass


def save():
    pickle.dump(ExpData, open("Requiem 2.0 - XP", "wb"))
    pickle.dump(NotificationAllowedChannels, open("Requiem 2.0 - Notif Channels", "wb"))


def load():
    global ExpData, NotificationAllowedChannels
    try:
        ExpData = pickle.load(open("Requiem 2.0 - XP", "rb"))
        NotificationAllowedChannels = pickle.load(open("Requiem 2.0 - Notif Channels", "rb"))
    except FileNotFoundError:
        ExpData = []
        NotificationAllowedChannels = []
        save()


#

# Variables
ExpData = []
NotificationAllowedChannels = []


#

# Commands
@client.event
async def on_ready():
    load()
    print("Bot is ready\n")


@client.command()
async def ping(ctx):
    _ping = round(client.latency * 1000, 2)
    _embed = discord.Embed(
        title=f"***Ping : `{_ping}ms`***",
        color=int((int(get_ping_colour(_ping)[0])) + (int(get_ping_colour(_ping)[1]) * 256)))
    await ctx.send(embed=_embed)


@client.event
async def on_message(message):
    if not message.author.bot:
        if message.author.id not in [x.userId for x in ExpData]:
            ExpData.append(Exp(message.author.id))
            await ExpData[-1].UpdateName()
        _fetchedUser = ExpData[[x.userId for x in ExpData].index(message.author.id)]

        # Updates user's name
        if f"{message.author.name}#{message.author.discriminator}" != _fetchedUser.username:
            await _fetchedUser.UpdateName()

        # Adding Exp and levelling up
        _fetchedUser.AddExp(message.content)
        if _fetchedUser.CanLevelUp():
            _fetchedUser.LevelUp()
            if message.channel.id in NotificationAllowedChannels:
                await _fetchedUser.SendLevelUp(message.channel)

        save()

    await client.process_commands(message)


@client.command()
async def exp_rank(ctx):
    apostrophe = "'"
    final = [
        f"{str(i).rjust(3, ' ')}. | {str(x.level).rjust(2, ' ')}. | {str(x.totalExp).rjust(6, apostrophe)} | {str(x.username).ljust(37, ' ')}"
        for i, x in enumerate(sorted(ExpData, key=lambda y: y.totalExp, reverse=True), start=1)]
    await ctx.send(embed=discord.Embed(
        title="***Exp Rankings***",
        description="```\nRANK | LVL |  EXP   | USER\n" + '\n'.join(final) + "```",
        color=random_colour()
    ))


@client.command()
async def get_lvl(ctx):
    try:
        if not ctx.message.mentions:
            fetched_user = ExpData[[x.userId for x in ExpData].index(ctx.message.author.id)]
        else:
            fetched_user = ExpData[[x.userId for x in ExpData].index(ctx.message.mentions[0].id)]
    except ValueError:
        new_user = Exp(ctx.message.mentions[0].id)
        ExpData.append(new_user)
        fetched_user = new_user
        await fetched_user.UpdateName()

    await ctx.send(embed=discord.Embed(
        title=f"**{fetched_user.username}'s Level**",
        description=f"```"
                    f"Rank  : {sorted(ExpData, key=lambda y: y.totalExp, reverse=True).index(fetched_user) + 1}\n"
                    f"Level : {fetched_user.level}\n"
                    f"Exp   : {fetched_user.currentExp}/{fetched_user.levelUpRequiredXp}```",
        colour=random_colour()
    ))


@has_permissions(manage_messages=True)
@client.command()
async def notification_channel_allow(ctx):
    if ctx.message.channel.id not in NotificationAllowedChannels:
        NotificationAllowedChannels.append(ctx.message.channel.id)
    else:
        await ctx.send("`The channel already has notifications allowed.`")


@has_permissions(manage_messages=True)
@client.command()
async def notification_channel_remove(ctx):
    if ctx.message.channel.id in NotificationAllowedChannels:
        NotificationAllowedChannels.remove(ctx.message.channel.id)
    else:
        await ctx.send("`The channel already doesn't have notifications allowed.`")


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


@client.command(pass_context=True, hidden=True)
async def cred(ctx):
    await ctx.send('<@517998886141558786> is my creator')


@client.command(pass_context=True, hidden=True)
@has_role("Bot Doctor")
async def shut_down(ctx):
    await ctx.send(f'{ctx.message.author.name} has shut me down.')
    print(ctx.message.author.name)
    await client.close()


@client.command(brief='Deletes messages',
                description='Deletes messages.\nOnly works for those with the manage messagse permission.\nFormat:\n.phurge {amount of messages to delete}')
@has_permissions(manage_messages=True)
async def phurge(ctx, *args):
    if type(args[0]) == str:
        args = int(args[0]) + 1
        await ctx.message.channel.purge(limit=args)
    else:
        await ctx.send(f'Purge amount argument incorrect.')


#

client.run(botToken)
