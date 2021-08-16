import Command, Data

role_system_servers = {
    500614426051739669: "Retards",
    718733572730781766: "Mushroom"
}


def server(guild_id):
    if guild_id in role_system_servers.keys():
        return role_system_servers[guild_id]
    else:
        return False


def all_stands(ctx):
    final = [f" {x.rjust(6, ' ')} : {ctx.guild.get_role(Data.stand_roles[x][0])}" for x in Data.stand_roles]
    return '```' + "\n".join(final) + '```'


def all_styles(ctx):
    final = [f" {x.rjust(6, ' ')} : {ctx.guild.get_role(Data.fighting_style_roles[x][0])}" for x in
             Data.fighting_style_roles]
    return '```' + "\n".join(final) + '```'


def init(client):
    @client.command()
    async def stand(ctx, args):
        if server(ctx.guild.id) == "Mushroom":
            stand_wanted = args
            if stand_wanted in [x for x in Data.stand_roles.keys()]:
                role = ctx.guild.get_role(Data.stand_roles[stand_wanted][0])
                await ctx.message.author.add_roles(role)
                await ctx.send(f"The role, {role}, has been assigned.")
            else:
                await ctx.send(f"Stand, {args}, was not found.")
                final = all_stands(ctx)
                await ctx.send(final)
        else:
            await Command.dispose_message(await ctx.send("Seems like you're using this in the wrong server :thinking:"))

    @client.command()
    async def stands(ctx):
        final = all_stands(ctx)
        await ctx.send(final)

    @client.command()
    async def styles(ctx):
        final = all_styles(ctx)
        await ctx.send(final)

    @client.command()
    async def style(ctx, args):
        if server(ctx.guild.id) == "Mushroom":
            style_wanted = args
            if style_wanted in [x for x in Data.fighting_style_roles.keys()]:
                role = ctx.guild.get_role(Data.fighting_style_roles[style_wanted][0])
                await ctx.message.author.add_roles(role)
                await ctx.send(f"The role, {role}, has been assigned.")
            else:
                await ctx.send(f"Fighting style, {args}, was not found.")
                final = all_styles(ctx)
                await ctx.send(final)
        else:
            await Command.dispose_message(await ctx.send("Seems like you're using this in the wrong server :thinking:"))
