import Formatting
import Dependencies
import discord
import json
from discord.ext.commands import has_permissions
from mcstatus import MinecraftServer
from uptime import uptime
import psutil
import random
import time


def verify_user(ctx):
    if ctx.message.author.id == Dependencies.author_id:
        return True


def find_in_message(content, target):
    info = ""
    for x in content:
        if x[0:len(target)] == target:
            info = x[len(target) + 1:]
    return info


def init(client):
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
                await Dependencies.delayed_delete(await ctx.send(final))
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
        await Dependencies.delayed_delete(await ctx.send(final))

    @client.command()
    async def ping(ctx):
        await ctx.message.delete()
        await Dependencies.dispose_message(await ctx.send(embed=discord.Embed(
            title=f"**Ping :** `{int(client.latency * 1000)}`",
            color=int((int(Formatting.get_ping_colour(int(client.latency * 1000))[0])) + (
                    int(Formatting.get_ping_colour(int(client.latency * 1000))[1]) * 256))
        )))

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

    @client.command()
    async def join(ctx, *args):
        if not verify_user(ctx):
            return
        args = tuple(args)
        channel = args[0]
        muted = ('y' in args[1].lower())
        await ctx.message.guild.change_voice_state(channel=await client.fetch_channel(channel), self_mute=muted)

    @client.command()
    async def disconnect(ctx):
        await ctx.message.guild.change_voice_state(channel=None)

    @client.command()
    async def toggle(ctx):
        try:
            await ctx.message.delete()
        except:
            pass
        if ctx.message.author.id == Dependencies.author_id:
            Dependencies.send_messages = not Dependencies.send_messages

    @client.command()
    async def fetch_pfp(ctx):
        if not ctx.message.mentions:
            selected_user = ctx.message.author
        else:
            selected_user = ctx.message.mentions[0]
        pfp = selected_user.avatar_url
        final = discord.Embed(title=f"**{selected_user.name}'s profile picture**",
                              color=Formatting.colour())
        final.set_image(url=pfp)
        await ctx.send(embed=final)

    @client.command()
    async def emoji_list(ctx, args="0"):
        await ctx.message.delete()
        try:
            index_wanted = int(args) - 1
        except ValueError:
            index_wanted = 0

        _emojis = [" | ".join([f"` {i.name} :`{str(i)}" for i in x]) for x in
                   [Dependencies.emojis[x:x + 37] for x in range(0, len(Dependencies.emojis), 37)]]

        if index_wanted not in range(0, len(_emojis)):
            final = discord.Embed(
                title="Index out of range.",
                description=f"Please select a number between 1 and {len(_emojis)}",
                colour=Formatting.colour()
            )
        else:
            final = discord.Embed(
                title=f"**Emojis ({len(Dependencies.emojis)})**",
                description=_emojis[index_wanted],
                colour=Formatting.colour()
            )
            final.set_footer(text=f"Showing page {index_wanted + 1} out of {len(_emojis)}")
        await Dependencies.dispose_message(await ctx.send(embed=final))

    @client.command()
    async def embed(ctx, *args):
        await ctx.message.delete()
        args = list(args)
        title = find_in_message(args, "title")
        description = find_in_message(args, "description")
        footer = find_in_message(args, "footer")
        try:
            colour = int(find_in_message(args, "colour"))
        except ValueError:
            colour = Formatting.colour()
        if ctx.message.attachments:
            image_url = ctx.message.attachments[0].url
        else:
            image_url = find_in_message(args, "image_url")
        disposable = ("y" in find_in_message(args, "disposable").lower())

        final = discord.Embed(
            title=title,
            description=description,
            colour=colour
        )
        final.set_image(url=image_url)
        final.set_footer(text=footer)

        msg = await ctx.send(embed=final)

        if disposable:
            await Dependencies.dispose_message(msg)

    @client.command(aliases=['mc_server', 'mc', 'retardsmp', 'server', 'minecraft'])
    async def server_info(ctx):
        with open('ajuna_Data/mc_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            ip = data['ip']
            server_name = data['server_name']

        try:
            server = MinecraftServer.lookup(ip)
            if server.status() is None:
                description = f"IP : `{ip}`\n"
                line = "⚫"
            else:
                mc_status = server.status()
                description = f"**IP :** `{ip}`\n\n" \
                              f"**Average ping** : `{random.randint(9000, 10000) / 1000}ms`\n" \
                              f"**Version :** {mc_status.version.name}\n" \
                              f"**Players :** {mc_status.players.online}/{mc_status.players.max}\n"
                line = "🟢"

                # Fetching players names
                try:
                    description += '\n'.join([f" \> {x.name}" for x in mc_status.players.sample])
                except Exception as e:
                    pass
                description += f"\n\n_Last checked : <t:{int(time.time())}:R> _"

            final = discord.Embed(title=f"{line}  **{server_name}**",
                                  description=description,
                                  color=Formatting.colour())
        except:
            final = discord.Embed(
                title=f"⚫ {server_name} is offline",
                description=f"**IP :** `{ip}`\n"
                            f"\n\n_Last checked : <t:{int(time.time())}:R> _"
            )
        await ctx.send(embed=final)

    @client.command()
    async def server_status(ctx):
        await ctx.message.delete()
        _mem = psutil.virtual_memory()
        final = discord.Embed(
            title="__**Server Status**__",
            description=f"**Latency**\n"
                        f"{round(client.latency * 1000, 2)}ms\n"
                        f"\n"
                        f"**CPU Usage**\n"
                        f"**`Used`** : {round(psutil.cpu_percent(), 2)}%\n"
                        f"\n"
                        f"**Memory usage**\n"
                        f"**`Total`** : {int(_mem.total / 1048576)} MiB\n"
                        f"**` Used`**  : {int(_mem.used / 1048576)} MiB   | _({int((_mem.used / _mem.total) * 100)}%)_\n"
                        f"**` Free`**  : {int(_mem.free / 1048576)} MiB   | _({int((_mem.free / _mem.total) * 100)}%)_\n\n"
                        f"**Server Uptime**\n"
                        f"{Formatting.uptime_string(uptime())}",
            color=int(
                int(Formatting.dynamic_color(_mem.used / _mem.total)[0] * 65536) + int(
                    Formatting.dynamic_color(_mem.used / _mem.total)[1] * 256)
            )
        )
        await Dependencies.dispose_message(await ctx.send(embed=final))

    @client.command()
    @has_permissions(manage_messages=True)
    async def purge(ctx, args):
        try:
            amount = int(args) + 1
            await ctx.message.channel.purge(limit=amount)
        except ValueError:
            await (await ctx.send(f'`Purge amount argument incorrect.`')).delete(delay=3)

    @client.command()
    @has_permissions(manage_messages=True)
    async def oos(ctx, deletable="none"):
        msg = await ctx.send("‎\n" * 100)
        if deletable != "none":
            await Dependencies.dispose_message(msg)

    @client.command()
    async def github(ctx):
        final = discord.Embed(
            title="**Github**",
            description="`discord-bots` : https://github.com/Asianerd/discord-bots\n"
                        "Invite link : https://lnk.gdn/vmnt",
            color=Formatting.colour()
        )
        final.set_footer(text="You can contribute by starring my repos!")
        await ctx.send(embed=final)

    @client.command()
    async def shut_down(ctx):
        if ctx.message.author.id in Dependencies.authorized_users:
            await ctx.send("ajuna_loli shutting down!")
            await client.logout()
        else:
            await Dependencies.delayed_delete(await ctx.send(
                embed=discord.Embed(title="**You are not an authorized user.**", color=Formatting.colour())), 3)

    @client.command()
    async def to_ascii(ctx):
        if ctx.message.attachments:
            image_attachment = ctx.message.attachments[0]
        else:
            await Dependencies.delayed_delete(
                await ctx.send(embed=discord.Embed(title="**Image not attached!**", color=Formatting.colour())), 3)
            return
        if not (any(image_attachment.filename.lower().endswith(x) for x in 'png/jpg/jpeg'.split("/"))):
            await Dependencies.delayed_delete(
                await ctx.send(embed=discord.Embed(title="**File format not supported.**", color=Formatting.colour())),
                3)
            return

        await image_attachment.save("_.ajuna - ToAscii.png")
        final = Formatting.convert_pixels_to_ascii()
        image_file = open("_.ajuna - AsciiOutput.txt", "w")
        image_file.write(final)
        image_file.close()
        image_file = discord.File("_.ajuna - AsciiOutput.txt")
        await ctx.send(file=image_file, content="**Ascii Image**")

    @client.command()
    async def cube(ctx):
        final = []
        moves = "R L U D F B R' L' U' D' F' B'".split()
        while len(final) < 8:
            wanted = random.choice(moves)
            if wanted[0] not in [x[0] for x in final[-3::]]:
                final.append(wanted)
        await ctx.send('`' + " ".join(final) + '`')

    @client.command()
    async def aussie(ctx, *args):
        message = ' '.join(args)
        message = message[-1::-1]
        final = ''.join([Dependencies.upside_down_letters[x] if x in Dependencies.upside_down_letters else x for x in message])
        await ctx.send(embed=discord.Embed(
            color=Formatting.colour(),
            title=final,
            description=""
        ))



    # @client.command()
    # async def social_credit(ctx, args):
    #     wanted_credits = 0
    #     try:
    #         wanted_credits = int(args[0])
    #     except:
    #         pass
    #     if wanted_credits == 0:
    #         await ctx.send(":1\\_: :2\\_: :3\\_:\n:4\\_: :5\\_: :6\\_:")
    #     elif wanted_credits > 0:
    #         pass
    #     else:
    #         pass
