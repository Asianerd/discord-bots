def init(client):
    listing = []

    @client.command
    async def view_shop(ctx):
        await ctx.send("None.")