import Data
import discord
import Experience, RoleSystem

async def dispose_message(message):
    Data.disposable_messages.append(message)
    await message.add_reaction(Data.reactions[0])


def init(client):
    RoleSystem.init(client)

    @client.command()
    async def ping(ctx):
        _ping = int(client.latency*1000)
        final = discord.Embed(title=f"**Ping :**{_ping}",
                              color=int((Data.get_ping_colour(_ping)[0]) + (Data.get_ping_colour(_ping)[1] * 256)
                              ))
        await dispose_message(await ctx.send(embed=final))

    # @client.command()
    # async def s(ctx, *args):
    #     try:
    #         role = ctx.guild.get_role(int(args[0][3:-1]))
    #         log[args[1]] = role.id
    #         await ctx.send(f"{role} : {role.id}")
    #         await ctx.send(f"```{log}```")
    #     except:
    #         await ctx.send("Error occured")
