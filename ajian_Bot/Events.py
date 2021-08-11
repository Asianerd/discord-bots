import Dependencies
import alexa_reply
import asyncio

def contains_emote(message):
    return ">[" in message


def locate_emote(message):
    try:
        start_index = message.index(">[")
        end_index = message.index("]")
    except ValueError:
        return False, None, (0, 0)
    emote_name = str(message[(start_index + 2):end_index]).strip()
    if emote_name in [x.name for x in Dependencies.emojis]:
        return True, Dependencies.emojis[([x.name for x in Dependencies.emojis].index(emote_name))], (
        start_index, end_index + 1)
    else:
        return False, None, (0, 0)


def init(client):
    @client.event
    async def on_ready():
        print("ajian_nedo is awake!")

    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        if contains_emote(message.content):
            emote = locate_emote(message.content)
            await message.delete()
            if emote[0]:
                await message.channel.send(f"{message.content[0:emote[2][0]]}{emote[1]}{message.content[emote[2][1]:]}")
            return
        if (message.content not in Dependencies.unsendable_content) and Dependencies.send_messages and (
                message.content[0] != Dependencies.command_prefix):
            if message.author.id == Dependencies.author_id:
                await message.delete()
                await message.channel.send(message.content)
        if message.content[0:5] == "ajuna":
            async with message.channel.typing():
                await asyncio.sleep(1)
            target = message.content[6::]
            reply = alexa_reply.reply(target, "ajuna_loli", "<@517998886141558786>")
            await message.reply(reply)
        await client.process_commands(message)

    @client.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return
        if reaction.message in Dependencies.disposable_messages:
            await reaction.message.delete()
