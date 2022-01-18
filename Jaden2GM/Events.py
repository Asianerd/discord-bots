import alexa_reply
import discord
from discord.ext import commands

import Dependencies
import Formatting


def init(client):
    @client.event
    async def on_ready():
        print('Jaden2GM is ready')

    @client.event
    async def on_message(message):
        if message.author.bot:
            return

        if 'jaden' in str(message.content).lower():
            if str(message.content)[0:5].lower() == 'jaden':
                await message.channel.send(alexa_reply.reply(message.content[6:], 'Sheep', '<@517998886141558786>'))

        await client.process_commands(message)

    @client.command()
    async def shut_down(ctx):
        if ctx.author.id == Dependencies.master_id:
            await ctx.send('Understood, shutting down.')
            await client.logout()
        else:
            await (await ctx.send(discord.Embed(
                title="You're not my master!",
                description="_This command can only be used by my creator._",

                colour=Dependencies.default_embed_colour
            ))).delete(delay=3)

    @client.command()
    async def ping(ctx):
        await ctx.send(embed=discord.Embed(
            title=f"**Ping :** `{int(client.latency * 1000)}`",
            color=int((int(Formatting.get_ping_colour(int(client.latency * 1000))[0])) + (
                    int(Formatting.get_ping_colour(int(client.latency * 1000))[1]) * 256))
        ))

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
                await (await ctx.send(final)).delete(delay=3)
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
        await (await ctx.send(final)).delete(delay=3)

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
