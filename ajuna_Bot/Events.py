import discord
import json
import time
import random
import asyncio
from mcstatus import MinecraftServer

from discord.ext import tasks, commands

import Dependencies


def init(bot: discord.Bot):
    @bot.event
    async def on_ready():
        print(f"{bot.user} is awake!")
        update_MC_info.start()

    @bot.event
    async def on_reaction_add(reaction, user):
        # await Economy.on_reaction_add(client, reaction, user)
        if user.bot:
            return
        if reaction.message in Dependencies.disposable_messages:
            await reaction.message.delete()

    @tasks.loop(seconds=60.0)
    async def update_MC_info():
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
                                  color=Dependencies.colour())
        except:
            final = discord.Embed(
                title=f"⚫ {server_name} is offline",
                description=f"**IP :** `{ip}`\n"
                            f"\n\n_Last checked : <t:{int(time.time())}:R> _"
            )
        channel = await bot.fetch_channel(data['server_channel'])
        try:
            message = await channel.fetch_message(data['server_message_id'])
            await message.edit(embed=final)
        except Exception as e:
            print(e)
            # message = await channel.send(embed=final)
            # data['server_message_id'] = message.id
            # with open('ajuna_Data/mc_data.json', 'w', encoding='utf-8') as file:
            #     json.dump(data, file, indent=4)
