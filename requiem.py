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


def load():
    global ExpData
    try:
        ExpData = pickle.load(open("Requiem 2.0 - XP", "rb"))
    except FileNotFoundError:
        ExpData = []
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
        color=int((int(get_ping_colour(_ping)[0] * 65536)) + (int(get_ping_colour(_ping)[1]) * 256)))
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
#

client.run(botToken)
