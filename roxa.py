import discord
from discord.ext import commands
from discord import state
import pickle
from pathlib import Path
import random

intents = discord.Intents().all()
client = commands.Bot(intents=intents, command_prefix="-")
save_file_path = Path(".") / "roxa_Data"
roxa_token = pickle.load(open(f"{save_file_path}/roxa - token", "rb"))

roxa_id = 743449031161806878
announcement_channel_id = 856210886938198016
# roxa_id = 517998886141558786
# announcement_channel_id = 508764064076529682
online_dialogue = []
offline_dialogue = []
wanker_id = 479595834418266114
# wanker_id = 517998886141558786


@client.event
async def on_ready():
    print("roxa simp is ready")
    load()


@client.event
async def on_member_update(before, after):
    if before.id == roxa_id:
        if before.status != after.status:
            channel = client.get_channel(announcement_channel_id)
            if after.status in [discord.state.Status.online, discord.state.Status.dnd, discord.state.Status.idle]:
                for x in online_dialogue:
                    await channel.send(x)
            if after.status == discord.state.Status.offline:
                for x in offline_dialogue:
                    await channel.send(x)


@client.command()
async def alter_online_dialogue(ctx, *args):
    global online_dialogue
    if ctx.message.author.id == wanker_id:
        online_dialogue = args
        save()
        newline = "\n"
        await (await ctx.send(f"Dialogue successfully changed to \n{newline.join(online_dialogue)}")).delete(delay=3)
    else:
        await (await ctx.send("You are not the wanker, and therefore have no access to this command.")).delete(delay=3)


@client.command()
async def alter_offline_dialogue(ctx, *args):
    global offline_dialogue
    if ctx.message.author.id == wanker_id:
        offline_dialogue = args
        save()
        newline = "\n"
        await (await ctx.send(f"Dialogue successfully changed to \n{newline.join(offline_dialogue)}")).delete(delay=3)
    else:
        await (await ctx.send("You are not the wanker, and therefore have no access to this command.")).delete(delay=3)


@client.command()
async def fetch_dialogue(ctx):
    on_d = "- " + ("\n - ".join(online_dialogue))
    off_d = "- " + ("\n - ".join(offline_dialogue))
    final = discord.Embed(title="**Stupid language**",
                          description=f"**Online Dialogue**\n{on_d}\n**Offline Dialogue**\n{off_d}",
                          color=random.randint(0x555555, 0xFFFFFF)
                          )
    final.set_footer(text="Bot's dialogue")
    await ctx.send(embed=final)


@client.command()
async def credit(ctx):
    await ctx.send("<@517998886141558786> made this cursed son of a bitch")
    await ctx.send("and <@479595834418266114> came up with this hella stupid idea")


@client.command()
async def commands(ctx):
    await ctx.send(
        "***Commands***\nalter_online_dialogue = Changes the online dialogue\nalter_offline_dialogue = Changes the offline dialogue\nfetch_dialogue = Fetches both online and offline dialogue")


def save():
    pickle.dump(online_dialogue, open(f"{save_file_path}/roxa - Online Dialogue", "wb"))
    pickle.dump(offline_dialogue, open(f"{save_file_path}/roxa - Offline Dialogue", "wb"))


def load():
    global online_dialogue, offline_dialogue
    try:
        online_dialogue = pickle.load(open(f"{save_file_path}/roxa - Online Dialogue", "rb"))
        offline_dialogue = pickle.load(open(f"{save_file_path}/roxa - Offline Dialogue", "rb"))
    except FileNotFoundError:
        pickle.dump([], open(f"{save_file_path}/roxa - Online Dialogue", "wb"))
        pickle.dump([], open(f"{save_file_path}/roxa - Offline Dialogue", "wb"))
        online_dialogue, offline_dialogue = [], []


client.run(roxa_token)
