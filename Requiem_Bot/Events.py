import Data


def init(client):
    @client.event
    async def on_ready():
        print("Requiem is ready")

    @client.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return
        if reaction.message in Data.disposable_messages:
            await reaction.message.delete()

