import discord
import json
import time
import random
import psutil
from uptime import uptime
from discord.commands import Option
from discord.ext import commands
from discord.ext.commands import Bot

import Dependencies
import Chemistry
import llm


def find_in_message(content, target):
    info = ""
    for x in content:
        if x[0:len(target)] == target:
            info = x[len(target) + 1:]
    return info


def init(bot: Bot, bot_state):
    @bot.slash_command()
    async def test(ctx):
        await ctx.respond(
            embed=discord.Embed(
                title="This is a test message. If you're seeing this, then the slash command module works!",
                description="There isn't much here...",
                colour=Dependencies.colour()
            ))
    
    @bot.slash_command(description="Displays information about the organic compound.")
    async def chem(ctx: discord.commands.ApplicationContext,
                   name: Option(str, "Name of an organic compound", required=True, default='methane')):
        final = discord.Embed(
            title=name,
            colour=Dependencies.colour()
        )
        if Chemistry.hydrocarbon(name):
            h = Chemistry.hydrocarbon(name)
            d = f"""
            **Homologous Series** : `{h['h_series']}`
            **Functional Group** : `{h['f_group']}`
            **Type of organic compound** : `{h['o_type']}`
            **General formula** : `{h['general_formula'][0]}; {h['general_formula'][1]}`
            **Number of carbon atoms** : `{h['carbon']}`
            
            **Chemical formula** : _{Chemistry.generate_name(name)}_
            
            **Structural formula**
            """
            result = Chemistry.image_generate(Chemistry.fix_input(name))
            final.set_image(url="attachment://image.png")
            if result:
                file = discord.File(f"chemistry_assets/library/{Chemistry.fix_input(name)}.png", filename="image.png")
            else:
                file = discord.File(f"chemistry_assets/media/ester.png", filename="image.png")
        else:
            d = f'{name} is not valid.'
        final.description = d
        await ctx.respond(
            file=file,
            embed=final
        )

    # @bot.slash_command(description="Fetches the minecraft server's status and players")
    # async def mc_server(ctx):
    #     with open('ajuna_Data/mc_data.json', 'r', encoding='utf-8') as file:
    #         data = json.load(file)
    #         ip = data['ip']
    #         server_name = data['server_name']
    #
    #     try:
    #         server = MinecraftServer.lookup(ip)
    #         if server.status() is None:
    #             description = f"IP : `{ip}`\n"
    #             line = "⚫"
    #         else:
    #             mc_status = server.status()
    #             description = f"**IP :** `{ip}`\n\n" \
    #                           f"**Average ping** : `{random.randint(9000, 10000) / 1000}ms`\n" \
    #                           f"**Version :** {mc_status.version.name}\n" \
    #                           f"**Players :** {mc_status.players.online}/{mc_status.players.max}\n"
    #             line = "🟢"
    #
    #             # Fetching players names
    #             try:
    #                 description += '\n'.join([f" \> {x.name}" for x in mc_status.players.sample])
    #             except Exception as e:
    #                 pass
    #             description += f"\n\n_Last checked : <t:{int(time.time())}:R> _"
    #
    #         final = discord.Embed(title=f"{line}  **{server_name}**",
    #                               description=description,
    #                               color=Dependencies.colour())
    #     except:
    #         final = discord.Embed(
    #             title=f"⚫ {server_name} is offline",
    #             description=f"**IP :** `{ip}`\n"
    #                         f"\n\n_Checked : <t:{int(time.time())}:R> _"
    #         )
    #     await ctx.respond(embed=final)

    @bot.slash_command()
    async def fetch_pfp(ctx: discord.commands.ApplicationContext,
                        name: Option(discord.Member, "Tag someone", required=False, default='')):
        if not name:
            selected_user = ctx.user
        else:
            selected_user = name
        pfp = selected_user.avatar.url
        final = discord.Embed(title=f"**{selected_user.name}'s profile picture**",
                              color=Dependencies.colour())
        final.set_image(url=pfp)
        await ctx.respond(embed=final)

    @bot.command()
    async def embed(ctx, *args):
        await ctx.message.delete()
        args = list(args)
        title = find_in_message(args, "title")
        description = find_in_message(args, "description")
        footer = find_in_message(args, "footer")
        try:
            colour = int(find_in_message(args, "colour"))
        except ValueError:
            colour = Dependencies.colour()
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
    
    @bot.slash_command()
    async def server(ctx: discord.commands.ApplicationContext):
#         **CPU** : `{round(psutil.cpu_percent(), 2)}%   {psutil.cpu_count()}x   {psutil.cpu_freq().current / 1000}Ghz`
# **RAM** : `[{Dependencies.ram_bar(_mem.used / _mem.total, 15)}]  ({int((_mem.used / _mem.total) * 100)}%)`
# `{int(_mem.used / 1048576)}/{int(_mem.total / 1048576)} Mib`
        
        _mem = psutil.virtual_memory();
        final = discord.Embed(
            title=f"**Server Info**",
            description=f"""**Location** : ` Sydney 📍 `
**Latency** : ` {round(bot.latency * 1000, 2)}ms 🟢 `
**Uptime** : ` {Dependencies.uptime_string(uptime())} `""",
            colour=Dependencies.colour()
            )
        final.add_field(
            name="RAM",
            value=f"` [{Dependencies.ram_bar(_mem.used / _mem.total, 15)}] `\n` {int(_mem.used / 1048576)}/{int(_mem.total / 1048576)} Mib  ({int((_mem.used / _mem.total) * 100)}%) `"
        )
        final.add_field(
            name="CPU",
            value=f"` {psutil.cpu_freq().current / 1000}Ghz  {round(psutil.cpu_percent(), 2)}% \n {psutil.cpu_count()}x Cores `",
            inline=True
        )
        final.set_footer(text=f"Asia Pacific (Sydney) ap-southeast-2 on {bot_state}")
        await ctx.respond(embed=final)

    @bot.slash_command(description="VERY VERY STUPID LLM; Based on Google's flan-t5-small dataset")
    async def ai(ctx: discord.commands.ApplicationContext,
                # Write me a story with an interesting plot.
                # Write me a story with a sci-fi plot.
                # Write me a sci-fi story with an interesting plot.
                prompt: Option(str, "Prompt", required=True, default='Write me a sci-fi story with an interesting plot.')):
        final = discord.Embed(
            title=prompt,
            description="*Generating response*",
            colour=Dependencies.colour()
        )
        final.set_footer(text=f"generated with google/flan-t5-small dataset")
        message = await ctx.respond(embed=final)
        final.description = f"{llm.generate(prompt)}"
        await message.edit_original_response(embed=final)
        