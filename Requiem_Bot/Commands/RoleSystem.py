from Requiem_Bot import Data, Command

role_system_servers = {
    500614426051739669: "Retards",
    718733572730781766: "Mushroom"
}


def server(guild_id):
    if guild_id in role_system_servers.keys():
        return role_system_servers[guild_id]
    else:
        return False


def init(client):
    @client.command()
    async def stand(ctx, args):
        if server(ctx.guild.id) == "Mushroom":
            stand_wanted = args
            role = ctx.guild.get_role(Data.stand_roles[stand_wanted][0])
            await ctx.message.author.add_roles(role)
            await ctx.send(f"The role, {role}, has been assigned.")
        else:
            await Command.dispose_message(await ctx.send("Seems like youre using this in the wrong server :thinking:"))

    @client.command()
    async def fetch_stands(ctx):
        final = [f" {x.rjust(6,' ')} : {ctx.guild.get_role(Data.stand_roles[x][0])}" for x in Data.stand_roles]
        await ctx.send('```'+"\n".join(final)+'```')
