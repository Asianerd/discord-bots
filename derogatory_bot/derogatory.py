import discord
from discord.ext import commands
from discord import Message
import random

bot = commands.Bot(intents=discord.Intents.all())
flag = False

@bot.event
async def on_message(msg: Message):
    if flag and (msg.author.id != 913370295325315092):
        await msg.reply(random.choice(['abbie', 'abeed', 'aboe', 'apeshit', 'apeshite', 'bean queen', 'beaner', 'beaners', 'blacky', 'buttermilk', 'c00n', 'c00nies', 'Camel jockey', 'ch1nk', 'chingchong', 'chink', 'chinky', 'cholo', 'coolie', 'coon', 'coon1es', 'cooni3s', 'coonie', 'coonies', 'coons', 'cotton picker', 'dago', 'darkass', 'darkfuck', 'darkie', 'darkshit', 'darktard', 'darky', 'dothead', 'dune coon', 'gook', 'greaser', 'groid', 'gyp', 'heeb', 'higg@', 'higg3r', 'higga', 'higger', 'higgers', 'injun', 'jap', 'jewboy', 'jigaboo', 'jigaboos', 'jigga', 'jiggaboo', 'jiggabooboo', 'jiggaboos', 'jiggabu', 'jiggas', 'jigger', 'jiggerboo', 'jiggerboos', 'jiggs', 'jiggyboo', 'jigro', 'jim crow', 'k!k3', 'k!ke', 'k..!ke', 'k1k3', 'k1ke', 'kike', 'kikes', 'klan', 'kneegrows', 'knickers', 'ku kluxer', 'kyke', 'm0ng0l0id', 'm0ngoloid', 'mong', 'mongoloid', 'mongrel', 'n1ckker', 'n1g3r', 'n1g3rz', 'n1gg@', 'n1gg@hs', 'n1gg3r', 'n1gg3rs', 'n1gga', 'n1ggah', 'n1ggahs', 'n1ggas', 'n1ggazes', 'n1gger', 'n1ggers', 'n1gguh', 'n3gro', 'negga', 'neggar', 'negr0', 'negro', 'negroes', 'negroid', 'niccer', 'nicka', 'nickas', 'nicker', 'nickk3r', 'nickker', 'nig', 'nig-nog', 'niga', 'nigah', 'nigasses', 'nigers', 'nigg@', 'nigg@hs', 'nigg@s', 'nigg@z', 'nigg@zzes', 'nigg3r', 'nigg3rs', 'nigg4h', 'nigg4hs', 'nigga', 'nigga lover', 'niggah', 'niggahs', 'niggahz', 'niggas', 'niggass', 'niggaz', 'niggazzes', 'nigger', 'nigger lover', 'niggers', 'niggerz', 'niggir', 'niggress', 'nigguh', 'nigguhs', 'nigguhz', 'niglet', 'nignigs', 'nignog', 'nigra', 'nigre', 'nigs', 'niguh', 'nikk3r', 'nikkas', 'nikker', 'nuckas', 'nuggets', 'oven dodger', 'paki', 'pancake face', 'porch monkey', 'raghead', 'ragheads', 'ragtard', 'redskin', 'rice monkey', 'sambo', 'sand nigger', 'sheister', 'shiester', 'shiesterfuck', 'shiesterfuckface', 'shiesterfuckhead', 'shiesterfucks', 'shylock', 'sl@nteye', 'slantard', 'slanteye', 'slanteye b1tch', 'slanteyes', 'slanteyeshit', 'slantfreak', 'slanty', 'spic', 'spicfuck', 'spick', 'spics', 'spicshit', 'spig', 'spik', 'spix', 'spook', 'spooks', 'tacohead', 'tar-baby', 'timber nigger', 'towelhead', 'towelheads', 'towelshithead', 'we1back', 'wet back', 'wetback', 'wetbacks', 'wigger', 'wop', 'wophead', 'zip in the wire', 'zipperhead']))

@bot.slash_command(description='toggles on/off the slurs')
async def toggle(ctx: discord.commands.ApplicationContext):
    global flag
    flag = not flag
    await ctx.respond(f"feature is now {(['off', 'on'][flag])}")

with open('derogatory_bot/token', 'r') as file:
    bot.run(file.read())
