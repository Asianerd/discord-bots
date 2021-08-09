import discord
from discord.ext import commands
from pathlib import Path
import pickle
import random

client = commands.Bot(command_prefix="--")
save_file_path = Path(".") / "ajian_pedo_Data"


def load(file_path, default):
    try:
        final = pickle.load(open(f"{save_file_path}/{file_path}", "rb"))
    except FileNotFoundError:
        final = default
        pickle.dump(final, open(f"{save_file_path}/{file_path}", "wb"))
    return final


def verified_user(ctx):
    return ctx.message.author.id in powered_users


# Users that have access to the bot's commands
powered_users = load("ajian_pedo - Powered Users", [517998886141558786, 859005581414236160])

# If the bot is guarding or not
guarding = False

# Users that are allowed into guarded channels
guarded_users = load("ajian_pedo - Guarded Users", [517998886141558786, 859005581414236160])

# Channels that are guarded
guarded_channels = load("ajian_pedo - Guarded Channels", [])

# If the bot replies everything with 'didnt ask', retardifies the message, or anything else
annoying = True

bot_token = pickle.load(open(f"{save_file_path}/ajian_pedo - Token", "rb"))


def save():
    pickle.dump(guarded_channels, open(f"{save_file_path}/ajian_pedo - Guarded Channels", "wb"))
    pickle.dump(guarded_users, open(f"{save_file_path}/ajian_pedo - Guarded Users", "wb"))
    pickle.dump(powered_users, open(f"{save_file_path}/ajian_pedo - Powered Users", "wb"))


async def set_presence():
    if guarding:
        await client.change_presence(activity=discord.Game(name="Guarding"))
    else:
        await client.change_presence(activity=None)


def retardify(message):
    final = ""
    _trigger = False
    for x in message.lower():
        if _trigger:
            final += x
        else:
            final += x.upper()
        _trigger = not _trigger
    return final


@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
async def guard(ctx):
    global guarding
    guarding = not guarding
    await ctx.message.delete()
    await set_presence()


@client.event
async def on_voice_state_update(member, before, after):
    try:
        if (after.channel.id in guarded_channels) and guarding and (not member.bot):
            if member.id not in guarded_users:
                await member.edit(voice_channel=None)
                await member.send("Not so fast buddy.\nThis voice channel is being guarded at the moment and will be "
                                  "opened after a short period of time.")
        else:
            return
    except AttributeError:
        pass


@client.event
async def on_message(message):
    if (not message.author.bot) and (annoying):
        final = [
            'didnt ask',
            retardify(message.content),
            'skill issue',
            'sounds like a you problem',
            'k'
        ][random.randint(0, 4)]
        await message.reply(final)
    await client.process_commands(message)


@client.command()
async def toggle_annoy(ctx):
    global annoying
    annoying = not annoying
    await (await ctx.send(f"Annoying : {annoying}")).delete(delay=3)


@client.command()
async def guard_user(ctx, user_id):
    if not verified_user(ctx):
        return
    try:
        wanted_user = int(user_id)
        if wanted_user not in guarded_users:
            guarded_users.append(wanted_user)
            final = "User successfully guarded."
        else:
            final = "User is already guarded."
    except ValueError:
        final = "Inputted ID was not a valid number."
    await (await ctx.send(final)).delete(delay=3)
    save()


@client.command()
async def unguard_user(ctx, user_id):
    if not verified_user(ctx):
        return
    try:
        wanted_user = int(user_id)
        if wanted_user in guarded_users:
            guarded_users.remove(wanted_user)
            final = "User successfully unguarded."
        else:
            final = "User was not found."
    except ValueError:
        final = "Inputted ID was not a valid number."
    await (await ctx.send(final)).delete(delay=3)
    save()


@client.command()
async def fetch_guarded_users(ctx):
    newline = "\n"
    final = discord.Embed(title="**Guarded Users**",
                          description=newline.join([f" - <@{x}>" for x in guarded_users]))
    await ctx.send(embed=final)


@client.command()
async def guard_channel(ctx, channel_id):
    if not verified_user(ctx):
        return
    try:
        wanted_channel = int(channel_id)
        if wanted_channel not in guarded_channels:
            guarded_channels.append(wanted_channel)
            final = "Channel successfully guarded."
        else:
            final = "Channel is already guarded."
    except ValueError:
        final = "Inputted ID was not a valid number."
    await (await ctx.send(final)).delete(delay=3)
    save()


@client.command()
async def unguard_channel(ctx, channel_id):
    if not verified_user(ctx):
        return
    try:
        wanted_channel = int(channel_id)
        if wanted_channel in guarded_channels:
            guarded_channels.remove(wanted_channel)
            final = "Channel successfully unguarded."
        else:
            final = "Channel is already unguarded."
    except ValueError:
        final = "Inputted ID was not a valid number."
    await (await ctx.send(final)).delete(delay=3)
    save()


@client.command()
async def fetch_guarded_channels(ctx):
    newline = "\n"
    final = discord.Embed(title="**Guarded Channels**",
                          description=newline.join([f" - <#{x}>" for x in guarded_channels]))
    await ctx.send(embed=final)


@client.command()
async def power_user(ctx, user_id):
    if not verified_user(ctx):
        return
    try:
        wanted_user = int(user_id)
        if wanted_user not in powered_users:
            powered_users.append(wanted_user)
            final = "User successfully powered."
        else:
            final = "User was not found."
    except ValueError:
        final = "Inputted ID was not a valid number."
    await (await ctx.send(final)).delete(delay=3)
    save()


@client.command()
async def unpower_user(ctx, user_id):
    if not verified_user(ctx):
        return
    try:
        wanted_user = int(user_id)
        if wanted_user in powered_users:
            powered_users.remove(wanted_user)
            final = "User successfully removed."
        else:
            final = "User was not found."
    except ValueError:
        final = "Inputted ID was not a valid number."
    await (await ctx.send(final)).delete(delay=3)
    save()


@client.command()
async def fetch_powered_users(ctx):
    newline = "\n"
    final = discord.Embed(title="**Powered Users**",
                          description=newline.join([f" - <@{x}>" for x in powered_users]))
    await ctx.send(embed=final)


client.run(bot_token)
