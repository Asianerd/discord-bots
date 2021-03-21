import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
import pickle
from pathlib import Path
import psutil
from uptime import uptime

client = commands.Bot(command_prefix=".", help_command=None)
saveFilePath = Path(".") / "bakupaku_Data"
botToken = pickle.load(open(f"{saveFilePath}/bakupaku - Token", "rb"))
creator = 517998886141558786
github_link = "https://github.com/Asianerd/discord-bots"


# Classes
class Exp:
    loggedMessagesAmount = 10

    def __init__(self, _user_id):
        self.userId = _user_id
        self.username = ''
        self.totalExp = 0
        self.level = 0
        self.currentExp = 0
        self.levelUpRequiredXp = 100

        self.lastSentMessage = ""
        self.lastSentMessages = []
        self.serverSpoken = {}

    def add_to_last_messages(self, msg_content):
        if msg_content not in self.lastSentMessages:
            self.lastSentMessages.append(msg_content)
            if len(self.lastSentMessages) >= Exp.loggedMessagesAmount:
                self.lastSentMessages = self.lastSentMessages[-Exp.loggedMessagesAmount:]

    def add_to_channels_spoken(self, guild_id, channel_id):
        if self.serverSpoken.get(guild_id) is None:
            self.serverSpoken[guild_id] = {}
        if self.serverSpoken[guild_id].get(channel_id) is None:
            self.serverSpoken[guild_id][channel_id] = 1
        else:
            self.serverSpoken[guild_id][channel_id] += 1

    def add_exp(self, msg_content):
        if msg_content not in self.lastSentMessages:
            added_exp = int(len(msg_content) * 2)
            if added_exp > 500:
                added_exp = 500
            self.currentExp += added_exp
            self.totalExp += added_exp
        self.add_to_last_messages(msg_content)

    def can_level_up(self):
        return self.currentExp >= self.levelUpRequiredXp

    def level_up(self):
        self.level += 1
        self.currentExp -= self.levelUpRequiredXp
        self.levelUpRequiredXp *= 2

    async def send_level_up(self, ctx, delete=True):
        _message = await ctx.send(embed=discord.Embed(title=f"{self.username} has leveled up!",
                                                      description=f"{self.level - 1} ==> {self.level}",
                                                      color=random_colour()))
        if delete:
            await _message.delete(delay=5)

    async def update_name(self):
        _name = await client.fetch_user(self.userId)
        self.username = f"{_name.name}#{_name.discriminator}"


class Server:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.name = ""

        self.level_up_channel = 0

    def update_name(self, _name):
        self.name = _name


#

# Functions
def random_colour():
    return random.randint(0x100000, 0xFFFFFF)


def dynamic_color(i):
    """Enter a float from 0-1 and will return red and green values accordingly,
    with 0 being fully green and 1 being fully red"""
    r = 255 * i
    g = 255 * (1-i)

    if r > 255:
        r = 255
    elif r < 0:
        r = 0

    if g > 255:
        g = 255
    elif g < 0:
        g = 0

    return int(r), int(g)


def uptime_string(enoch_time):
    if enoch_time > 3600:
        hour = enoch_time // 3600
        minute = (enoch_time / 60) - (int(hour) * 60)
        return f"{int(hour)}h {int(minute)}m"
    else:
        minute = enoch_time / 60
        second = enoch_time - (int(minute) * 60)
        return f"{int(minute)}m {int(second)}s"


def add_to_log():
    pass


def save():
    pickle.dump(ExpData, open(f"{saveFilePath}/bakupaku - XP", "wb"))
    pickle.dump(NotificationAllowedChannels, open(f"{saveFilePath}/bakupaku - Notification Channels", "wb"))
    pickle.dump(Servers, open(f"{saveFilePath}/bakupaku - Servers", "wb"))


def load():
    global ExpData, NotificationAllowedChannels, Servers
    try:
        ExpData = pickle.load(open(f"{saveFilePath}/bakupaku - XP", "rb"))
        NotificationAllowedChannels = pickle.load(open(f"{saveFilePath}/bakupaku - Notification Channels", "rb"))
        Servers = pickle.load(open(f"{saveFilePath}/bakupaku - Servers", "rb"))
    except FileNotFoundError:
        ExpData = []
        NotificationAllowedChannels = []
        Servers = []
        save()


async def disposable_message(msg, reaction):
    DisposableMessages.append(msg)
    await msg.add_reaction(reaction)


def make_server_object(guild_id):
    global Servers
    if guild_id not in [x.guild_id for x in Servers]:
        Servers.append(Server(guild_id))


def get_server_object(guild_id):
    return Servers[[x.guild_id for x in Servers].index(guild_id)]


def is_creator(user_id):
    return user_id == creator


#

# Variables
Servers = []
ExpData = []
Commands = [[["exp_rank", "Shows the experience ranking."],
             ["get_lvl", "Shows the level and current progress of the mentioned user."]],
            [["notification_channel_allow",
              "Enables notifications in the channel. Will only send notifications if there isnt a dedicated "
              "notification channel."],
             ["notification_channel_remove",
              "Disables notifications in the channel. Will only send notifications if there isnt a dedicated "
              "notification channel."],
             ["check_notification", "Shows whether notifications has been enabled for the channel."],
             ["set_level_channel", "Sets the channel as the dedicated level-up notification channel."],
             ["remove_level_channel", "Removes the dedicated level-up feature from the server."],
             ["phurge",
              "Purges the selected amount of messages.(Named phurge to avoid multiple bots doing the same thing)"],
             ["ban", "Bans the mentioned user."],
             ["kick", "Kicks the mentioned user."]],
            [["oos",
              "Out of sight. Outputs a giant block of nothing to 'erase' chat.(Add letters or anything after the 'oos' "
              "to make the outputted oos disposable)"],
             ["fetch_pfp", "Returns the mentioned user's profile picture."],
             ["get_info", "Returns information, such as his/her most active server"],
             ["server_status","Returns information about the CPU and memory usage of the server."],
             ["github","Provides a link to the project's github repo :D"]
             ]]
NotificationAllowedChannels = []
DisposableMessages = []
Emojis = ["\N{WASTEBASKET}"]


#

# Events
@client.event
async def on_ready():
    load()
    print("Bot is ready\n")


@client.command()
async def ping(ctx):
    _ping = round(client.latency * 1000, 2)
    _embed = discord.Embed(
        title=f"***Ping : `{_ping}ms`***",
        color=int(int(dynamic_color(_ping/500)[0]*65536) + int(dynamic_color(_ping/500)[1]) * 256)
    )
    message = await ctx.send(embed=_embed)
    await disposable_message(message, Emojis[0])
    await ctx.message.delete()


@client.event
async def on_message(message):
    if message.author.bot:
        return
    # Makes the server object (if it doesnt exist yet)
    make_server_object(message.guild.id)
    _server = get_server_object(message.guild.id)

    _server.update_name(message.guild.name)

    if message.author.id not in [x.userId for x in ExpData]:
        ExpData.append(Exp(message.author.id))
        await ExpData[-1].update_name()
    _fetchedUser = ExpData[[x.userId for x in ExpData].index(message.author.id)]

    # Updates user's name
    if f"{message.author.name}#{message.author.discriminator}" != _fetchedUser.username:
        await _fetchedUser.update_name()

    # Adding Exp and levelling up
    _fetchedUser.add_exp(message.content)
    if _fetchedUser.can_level_up():
        _fetchedUser.level_up()
        if _server.level_up_channel != 0:
            await _fetchedUser.send_level_up(_server.level_up_channel, False)  # Send to a specified channel
        else:
            if message.channel.id in NotificationAllowedChannels:
                await _fetchedUser.send_level_up(message.channel)  # Send to the channel the user sent message

    # Increase count for the current channel
    _fetchedUser.add_to_channels_spoken(message.guild.id, message.channel.id)

    save()
    await client.process_commands(message)


@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.message in DisposableMessages:
        await reaction.message.delete()


#

# Commands

@client.command()
async def help(ctx):
    await ctx.message.delete()
    newline = "\n"
    embed = discord.Embed(
        title="__**Commands**__",
        description=f"\n\n**Experience**\n{newline.join([f'{x[0]} : {x[1]}' for x in Commands[0]])}"
                    f"\n\n**Moderation**\n{newline.join([f'{x[0]} : {x[1]}' for x in Commands[1]])}"
                    f"\n\n**Others**\n{newline.join([f'{x[0]} : {x[1]}' for x in Commands[2]])}",
        color=random_colour()
    )
    await disposable_message(await ctx.send(embed=embed), Emojis[0])


@client.command()
async def server_status(ctx):
    await ctx.message.delete()
    _mem = psutil.virtual_memory()
    final = discord.Embed(
        title="__**Server Status**__",
        description=f"**Latency**\n"
                    f"{round(client.latency * 1000, 2)}ms\n"
                    f"\n\n"
                    f"**CPU Usage**\n"
                    f"**`Used`** : {round(psutil.cpu_percent(),2)}%\n"
                    f"\n\n"
                    f"**Memory usage**\n"
                    f"**`Total`** : {int(_mem.total / 1048576)} MiB\n"
                    f"**` Used`**  : {int(_mem.used / 1048576)} MiB   | _({int((_mem.used / _mem.total) * 100)}%)_\n"
                    f"**` Free`**  : {int(_mem.free / 1048576)} MiB   | _({int((_mem.free/_mem.total)*100)}%)_\n\n"
                    f"**Server Uptime**\n"
                    f"{uptime_string(uptime())}",
        color=int(
            int(dynamic_color(_mem.used/_mem.total)[0]*65536) + int(dynamic_color(_mem.used/_mem.total)[1] * 256)
                  )
    )
    await disposable_message(await ctx.send(embed=final), Emojis[0])


@client.command(aliases=["xp_rank", "experience_rank"])
async def exp_rank(ctx):
    apostrophe = "'"
    users = [
        f"{str(i).rjust(3, ' ')}. | {str(x.level).rjust(2, ' ')}. | {str(x.totalExp).rjust(6, apostrophe)} | "
        f"{str(x.username).ljust(37, ' ')} "
        for i, x in enumerate(sorted(ExpData, key=lambda y: y.totalExp, reverse=True)[0:30], start=1)]

    final = discord.Embed(
        title="***Exp Rankings***",
        description="```\nRANK | LVL |  EXP   | USER\n" + '\n'.join(users) + "```",
        color=random_colour())
    final.set_footer(text=f"Showing {len(users)} out of {len(ExpData)}")

    await ctx.message.delete()
    message = await ctx.send(embed=final)
    await disposable_message(message, Emojis[0])


@client.command(aliases=["get_level", "level", "lvl", "fetch_lvl", "fetch_level"])
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
        await fetched_user.update_name()

    message = await ctx.send(embed=discord.Embed(
        title=f"**{fetched_user.username}'s Level**",
        description=f"```"
                    f"Rank  : {sorted(ExpData, key=lambda y: y.totalExp, reverse=True).index(fetched_user) + 1}\n"
                    f"Level : {fetched_user.level}\n"
                    f"Exp   : {fetched_user.currentExp}/{fetched_user.levelUpRequiredXp}```",
        colour=random_colour()
    ))
    await ctx.message.delete()
    await disposable_message(message, Emojis[0])


@has_permissions(manage_messages=True)
@client.command()
async def notification_channel_allow(ctx):
    if ctx.message.channel.id not in NotificationAllowedChannels:
        NotificationAllowedChannels.append(ctx.message.channel.id)
        message = await ctx.send("`Notifications for this channel has been allowed.`")
    else:
        message = await ctx.send("`The channel already has notifications allowed.`")
    await ctx.message.delete(delay=3)
    await message.delete(delay=3)


@has_permissions(manage_messages=True)
@client.command()
async def notification_channel_remove(ctx):
    if ctx.message.channel.id in NotificationAllowedChannels:
        NotificationAllowedChannels.remove(ctx.message.channel.id)
        message = await ctx.send("`Notifications for this channel has been blocked.`")
    else:
        message = await ctx.send("`The channel already doesn't have notifications allowed.`")
    await ctx.message.delete(delay=3)
    await message.delete(delay=3)


@client.command()
async def check_notification(ctx):
    if ctx.message.channel.id in NotificationAllowedChannels:
        message = await ctx.send("`Notifications are allowed in this channel.`")
    else:
        message = await ctx.send("`Notifications are not allowed in this channel.`")
    await ctx.message.delete(delay=5)
    await message.delete(delay=5)


@client.command()
@has_permissions(manage_messages=True)
async def set_level_channel(ctx):
    await ctx.message.delete()
    _guild = get_server_object(ctx.guild.id)
    _guild.level_up_channel = ctx.message.channel
    await (await ctx.send("`Channel set for level-up notifications.`")).delete(delay=5)


@client.command()
@has_permissions(manage_messages=True)
async def remove_level_channel(ctx):
    await ctx.message.delete()
    _guild = get_server_object(ctx.guild.id)
    _guild.level_up_channel = 0
    await (await ctx.send("`Channel set for no level-up notifications.`")).delete(delay=5)


@client.command(pass_context=True, brief="Changes the bot's status",
                description="Changes the bot description.\nFormat:\ng - Game\nl - Listening\ns - Streaming\nw - "
                            "Watching")
async def change_pres(ctx, *args):
    if not is_creator(ctx.message.author.id):
        return
    acts = ['g', 'l', 's', 'w']
    wanted_act = args[0]
    wanted_subject = args[1]
    if wanted_act == acts[2]:
        if len(args) >= 3:
            wanted_link = args[2]
        else:
            await (await ctx.send(
                f'Arguments insufficient or incorrect  - Streaming status needs to be provided with a url')).delete(
                delay=3)
            return
    else:
        wanted_link = ''
    if wanted_act in acts:
        if wanted_act == acts[0]:
            await client.change_presence(activity=discord.Game(name=wanted_subject))
            message = await ctx.send(f'Activity set to **Playing {wanted_subject}**')
        elif wanted_act == acts[1]:
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening, name=wanted_subject))
            message = await ctx.send(f'Activity set to **Listening to {wanted_subject}**')
        elif wanted_act == acts[2]:
            await client.change_presence(activity=discord.Streaming(name=wanted_subject, url=wanted_link))
            message = await ctx.send(f'Activity set to **Streaming {wanted_subject} at {wanted_link}**')
        else:
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=wanted_subject))
            message = await ctx.send(f'Activity set to **Watching {wanted_subject}**')
        await disposable_message(message, Emojis[0])
    else:
        await (await ctx.send(f'Arguments insufficient or incorrect   -{args, wanted_act, wanted_subject}')).delete(
            delay=3)
        await ctx.message.delete()


@client.command(pass_context=True, hidden=True)
async def change_stat(ctx, args):
    if not is_creator(ctx.message.author.id):
        return
    if args in ['do', 'on', 'id', 'in']:
        if args == 'do':
            await client.change_presence(status=discord.Status.do_not_disturb)
        elif args == 'on':
            await client.change_presence(status=discord.Status.online)
        elif args == 'id':
            await client.change_presence(status=discord.Status.idle)
        else:
            await client.change_presence(status=discord.Status.invisible)
    else:
        await (await ctx.send('`Parameter not in activity list`')).delete(delay=3)
    await ctx.message.delete()


@client.command(pass_context=True, hidden=True)
async def cred(ctx):
    await ctx.send(f'<@{creator}> is my creator')


@client.command()
async def github(ctx):
    final = discord.Embed(
        title="__**Github**__",
        description=f"_Anyone is welcome to contribute!_\n"
                    f"{github_link}",
        color=random_colour()
    )
    final.set_footer(text="discord-bots is a product of Asianerd")
    await ctx.send(embed=final)


@client.command(pass_context=True, hidden=True)
async def shut_down(ctx):
    if not is_creator(ctx.message.author.id):
        return
    await ctx.send(f'<@{ctx.message.author.id}> has shut me down.')
    print(ctx.message.author.name)
    await client.close()


@client.command(aliases=["purge"],
                brief='Deletes messages',
                description='Deletes messages.\nOnly works for those with the manage messages '
                            'permission.\nFormat:\n.phurge {amount of messages to delete}')
@has_permissions(manage_messages=True)
async def phurge(ctx, *args):
    try:
        amount = int(args[0]) + 1
        await ctx.message.channel.purge(limit=amount)
    except ValueError:
        await (await ctx.send(f'`Purge amount argument incorrect.`')).delete(delay=3)


@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, args="none"):
    if not ctx.message.mentions:
        await ctx.send("`No user mentioned.`")
    else:
        banned_user = ctx.message.mentions[0]
        if args == "none":
            await banned_user.ban()
        else:
            await banned_user.ban(reason=args)
        await (await ctx.send("`User successfully banned.`")).delete(delay=5)


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, args="none"):
    if not ctx.message.mentions:
        await ctx.send("`No user mentioned.`")
    else:
        kicked_user = ctx.message.mentions[0]
        if args == "none":
            await kicked_user.kick()
        else:
            await kicked_user.kick(reason=args)
        await (await ctx.send("`User successfully kicked.`")).delete(delay=5)


#

# Random commands
@has_permissions(manage_messages=True)
@client.command()
async def oos(ctx, args="none"):
    message = await ctx.send('‎\n'*200)
    if args != "none":
        await disposable_message(message, Emojis[0])


@client.command(aliases=["get_pfp", "profile_pic", "pfp"])
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
async def get_info(ctx):
    try:
        if not ctx.message.mentions:
            user_object = ExpData[[x.userId for x in ExpData].index(ctx.message.author.id)]
            _user = ctx.message.author
        else:
            user_object = ExpData[[x.userId for x in ExpData].index(ctx.message.mentions[0].id)]
    except ValueError:
        new_user = Exp(ctx.message.mentions[0].id)
        ExpData.append(new_user)
        user_object = new_user
        await user_object.update_name()

    if not ctx.message.mentions:
        _user = ctx.message.author
    else:
        _user = ctx.message.mentions[0]

    try:
        most_spoken_server = (await client.fetch_guild([x for _, x in sorted(
            zip([sum([user_object.serverSpoken[x][y] for y in user_object.serverSpoken[x]]) for x in
                 user_object.serverSpoken],
                [x for x in user_object.serverSpoken]), reverse=True)][0]))
    except IndexError:
        most_spoken_server = "None"

    embed = discord.Embed(
        title=f"{_user.name}",
        description=f"**Most active in** : *{most_spoken_server}*\n"
                    f"```"
                    f"Rank  : {sorted(ExpData, key=lambda y: y.totalExp, reverse=True).index(user_object) + 1}\n"
                    f"Level : {user_object.level}\n"
                    f"Exp   : {user_object.currentExp}/{user_object.levelUpRequiredXp}```",
        color=random_colour()
    )
    embed.set_image(url=_user.avatar_url)
    await ctx.send(embed=embed)


#
# Code to sort by dict value
# [x for _, x in sorted(zip([sum([data[x][y] for y in data[x]]) for x in data], [x for x in data]), reverse=True)][0]

# Testing commands

#

client.run(botToken)
