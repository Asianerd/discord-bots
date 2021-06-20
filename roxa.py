import discord
from discord.ext import commands
from discord import state
import pickle
from pathlib import Path

intents = discord.Intents().all()
client = commands.Bot(intents=intents, command_prefix="-", help_command=None)
save_file_path = Path(".") / "roxa_Data"
roxa_token = pickle.load(open(f"{save_file_path}/roxa - token","rb"))

#roxa_id = 743449031161806878
#announcement_channel_id = 856210886938198016
roxa_id = 517998886141558786
announcement_channel_id = 508764064076529682

@client.event
async def on_ready():
    print("roxa simp is ready")


@client.event
async def on_member_update(before, after):
    if before.id == roxa_id:
        if before.status != after.status:
            channel = client.get_channel(announcement_channel_id)
            if after.status in [discord.state.Status.online, discord.state.Status.dnd, discord.state.Status.idle]:
                await channel.send(f"LETS GO <@{roxa_id}> ONLINE")
                await channel.send("Hey roxa! How's your day going? Good to hear that! :pikalove: My day isn't going very well though. Cat died, dog died, fish died, mom died, dad died, grandma died, got fired from my job, got raided by the IRS, my kids hate me, my wife left me, my car exploded, my train derailed, plane crashed into a building, my house burnt down, my drug dealer got arrested, but thats okay. Why? because my favourite e-girl roxa is online. Have the rest of my bank account. Accept my offering my queen :Rushia_Love:  Oh and my credit card is 5262260061602530. Anything for you my darling baby honey cutie wifey queen :zeroTwoHeart: As long as you are online, I will always be happy :peepoLove: And i will give everything to you, for you, only you. I love you roxa :ShibaHeart:")
            if after.status == discord.state.Status.offline:
                await channel.send("Our queen went offline :((")


@client.command()
async def credit(ctx):
    await ctx.send("<@517998886141558786> made this cursed son of a bitch")


client.run(roxa_token)
