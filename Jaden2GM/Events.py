import math
import alexa_reply
import discord
from discord.ext import commands

import Dependencies
import Formatting
import Quest


def find_in_message(key, message):
    for x in message:
        if x[0:len(key)] == key:
            return x[len(key) + 1:]
    return False


def init(client):
    @client.event
    async def on_ready():
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="over T(G)evyat"))
        print('Jaden2GM is ready')

    @client.event
    async def on_message(message):
        if message.author.bot:
            return

        if 'jaden' in str(message.content).lower():
            if str(message.content)[0:5].lower() == 'jaden':
                await message.reply(alexa_reply.reply(message.content[6:], 'Sheep', '<@517998886141558786>'))

        await client.process_commands(message)

    @client.command()
    async def shut_down(ctx):
        if ctx.author.id == Dependencies.master_id:
            await ctx.send('Understood, shutting down.')
            await client.logout()
        else:
            await (await ctx.send(embed=discord.Embed(
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
        arg_dict = {
            'do': discord.Status.do_not_disturb,
            'on': discord.Status.online,
            'id': discord.Status.idle,
            'in': discord.Status.invisible
        }

        if args in arg_dict.keys():
            await client.change_presence(status=arg_dict['args'])
        else:
            await ctx.send('Argument not in activity list')

    @client.command()
    async def quests(ctx, args='1'):
        try:
            page = int(args) - 1
            if (page < int(math.ceil(len(Quest.Quest.quests) / Dependencies.quests_per_page))) and (page >= 0):
                pass
            else:
                raise ValueError
        except ValueError:
            await ctx.send(embed=discord.Embed(
                title="Invalid page number!",
                description=f"Use a page number from [1 - {int(math.ceil(len(Quest.Quest.quests) / Dependencies.quests_per_page))}]",
                colour=Dependencies.error_embed_colour
            ))
            return

        final = discord.Embed(
            title="Quests",
            description=('\n'.join([x.get_info() for x in Quest.Quest.fetch_split_quests(page)])),
            colour=Formatting.colour()
        )

        temp = "{id}"
        final.set_footer(text=f'(quest {temp}) for more info\nPage {page + 1} of {int(math.ceil(len(Quest.Quest.quests) / Dependencies.quests_per_page))}')
        await ctx.send(embed=final)

    @client.command()
    async def quest(ctx, args='not_given'):
        try:
            if args == 'not_given':
                raise ValueError
            target_id = int(args)
            if target_id in [x.id for x in Quest.Quest.quests]:
                pass
            else:
                raise ValueError
        except ValueError:
            newline = "\n"
            await ctx.send(embed=discord.Embed(
                title="Invalid ID",
                description=f"Pick from one of these IDS : \n{newline.join([f'- {x.id} : {x.name}' for x in Quest.Quest.quests])}",
                colour=Dependencies.error_embed_colour
            ))
            return

        target: Quest.Quest = [x for x in Quest.Quest.quests if x.id == target_id][0]
        final = discord.Embed(
            title=target.name,
            color=Dependencies.default_embed_colour
        )
        final.add_field(
            name="Info",
            value=f"{target.description}\n"
                  f"\n"
                  f"**Rewards :**\n"
                  f"- {target.rewards}\n"
                  f"\n"
                  f"Ongoing : **__{'Yes' if target.is_ongoing else 'No'}__**"
        )
        final.add_field(
            name=f"Finishers - {len(target.users_completed)}",
            value=''.join([f'- <@{x}>\n' for x in target.users_completed]) if (len(target.users_completed) != 0) else 'None'
        )
        await ctx.send(embed=final)

    @commands.has_permissions(administrator=True)
    @client.command()
    async def add_quest(ctx, *args):
        name = find_in_message('name', args)
        description = find_in_message('description', args)
        rewards = find_in_message('rewards', args)
        if (not name) or (not rewards):
            await ctx.send(embed=discord.Embed(
                title='Quest name or rewards is not given!',
                colour=Dependencies.error_embed_colour
            ))
            return

        x = Quest.Quest(
            name,
            description if description else '',
            rewards,
            0,
            0
        )
        await ctx.send(embed=discord.Embed(
            title="Quest added!",
            colour=Dependencies.success_embed_colour
        ))
        await quests(ctx, args=str(int(math.ceil(len(Quest.Quest.quests) / Dependencies.quests_per_page))))
        Quest.Quest.save()

    @commands.has_permissions(administrator=True)
    @client.command(hidden=True)
    async def complete_quest(ctx, *args):
        user = [x for x in args if x[0] == '<'][0]
        quest_id = int([x for x in args if x[0] != '<'][0])

        result = Quest.Quest.complete_quest(int(''.join([i for i in user if i in '1 2 3 4 5 6 7 8 9 0'.split()])), quest_id)
        if result[0]:
            target: Quest.Quest = [x for x in Quest.Quest.quests if x.id == quest_id][0]

        await ctx.send(embed=discord.Embed(
            title=result[1],
            description=f"Quest name : {target.name}" if result[0] else '',
            colour=Dependencies.success_embed_colour if result[0] else Dependencies.error_embed_colour
        ))
        Quest.Quest.save()

    @commands.has_permissions(administrator=True)
    @client.command()
    async def delete_quest(ctx, args='not_given'):
        try:
            quest_id = int(args)
            if quest_id in [x.id for x in Quest.Quest.quests]:
                pass
            else:
                raise ValueError
        except ValueError:
            await ctx.send(embed=discord.Embed(
                title="Invalid ID",
                colour=Dependencies.error_embed_colour
            ))
            return

        target_quest = [x for x in Quest.Quest.quests if x.id == quest_id][0]
        name = target_quest.name
        Quest.Quest.quests.remove(target_quest)
        await ctx.send(embed=discord.Embed(
            title="Quest removed sucessfully",
            description=f"Name : {name}",
            colour=Dependencies.success_embed_colour
        ))
        Quest.Quest.save()

