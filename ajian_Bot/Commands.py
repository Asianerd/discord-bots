import Formatting
import Dependencies
import discord


async def delayed_delete(message, delay=3):
    await message.delete(delay=delay)


async def dispose_message(ctx):
    Dependencies.disposable_messages.append(ctx)
    await ctx.add_reaction(Dependencies.reactions[0])


def verify_user(ctx):
    if ctx.message.author.id == Dependencies.author_id:
        return True

def find_in_message(content,target):
    info = ""
    for x in content:
        if x[0:len(target)] == target:
            info = x[len(target)+1:]
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
        await dispose_message(await ctx.send(embed=discord.Embed(
            title=f"**Ping :** `{int(client.latency * 1000)}`",
            color=int((int(Formatting.get_ping_colour(int(client.latency * 1000))[0])) + (
                    int(Formatting.get_ping_colour(int(client.latency * 1000))[1]) * 256))
        )))
        print(int((int(Formatting.get_ping_colour(287)[0])) + (int(Formatting.get_ping_colour(287)[1]) * 256)))

    @client.command(pass_context=True, hidden=True)
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
    async def fetch_emojis(ctx):
        await ctx.message.delete()
        old = len(Dependencies.emojis)
        for x in ctx.message.guild.emojis:
            if x not in Dependencies.emojis:
                Dependencies.emojis.append(x)
        await delayed_delete(await ctx.send(f"Gathering done - [{len(Dependencies.emojis)-old}]"))

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
                title="**Emojis**",
                description=_emojis[index_wanted],
                colour=Formatting.colour()
            )
        await dispose_message(await ctx.send(embed=final))


    @client.command()
    async def embed(ctx, *args):
        await ctx.message.delete()
        args = list(args)
        title = find_in_message(args, "title")
        description = find_in_message(args, "description")
        footer = find_in_message(args,"footer")
        try:
            colour = int(find_in_message(args,"colour"))
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
            await dispose_message(msg)
