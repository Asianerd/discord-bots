import discord
from discord.ext import commands
from discord.ext.commands import has_role, has_permissions, has_any_role
import random
import time
import pickle

"""
"""


class Exp:
    def __init__(self):
        self.current_exp = 0
        self.total_exp = 0
        self.required_level_exp = 100
        self.level = 0
        self.has_leveled_up = False

    def add_exp(self, msg_content):
        added_exp = int(len(msg_content) * 2)
        if added_exp > 500:
            added_exp = 500
        self.current_exp += added_exp
        self.total_exp += added_exp

    def check_level_up(self, chan_msg, user_indx):
        if self.required_level_exp <= self.current_exp:
            self.level += 1
            self.current_exp -= self.required_level_exp
            self.required_level_exp *= 2
            self.has_leveled_up = True

    def send_chat_level_up(self):
        if self.has_leveled_up:
            self.has_leveled_up = False
            return True


class Tournaments:
    def __init__(self, guildid, participants, tournament_starter_id):
        self.guild = guildid
        self.participants = participants
        random.shuffle(participants)
        self.tmnt_starter_id = tournament_starter_id
        self.round_index = 0
        self.winners = []

        self.p_text_all = []
        for x in participants:
            self.p_text_all.append(str(participants.index(x) + 1) + '. ' + str(x))
        # 1. name
        # 2. name

        self.matched_up_participants_text_list = []
        for x in range(int(len(self.participants) / 2)):
            self.matched_up_participants_text_list.append(
                f'{x + 1}. **{participants[x * 2]}** VS **{participants[(x * 2) + 1]}**')
        # ['1. name VS name','2. name VS name']

        self.matched_up_participants_list = []
        for x in range(int(len(self.participants) / 2)):
            self.matched_up_participants_list.append([self.participants[x * 2], self.participants[(x * 2) + 1]])
        # [['name','name'],['name','name']]

        self.matched_up_text = '\n'.join(self.matched_up_participants_text_list)
        # 1. name VS name
        # 2. name VS name

        self.matched_up_text_with_wins = ''
        for x in range(len(self.matched_up_participants_text_list)):
            if x == self.round_index:
                self.matched_up_text_with_wins += '\n' + str(
                    self.matched_up_participants_text_list[x]) + '     Current match'
            elif x - 1 == self.round_index:
                self.matched_up_text_with_wins += '\n' + str(
                    self.matched_up_participants_text_list[x]) + '     Next match'
        # 1. name VS name   Winner - {name}
        # 2. name VS name   Current match
        # 3. name VS name   Next match

        self.current_round = self.matched_up_participants_text_list[self.round_index]
        # 1. name VS name

    def set_round_result(self, if_win):
        if self.round_index < len(self.matched_up_participants_list):
            if if_win:
                self.winners.append(self.matched_up_participants_list[self.round_index][0])
                self.round_index += 1
            else:
                self.winners.append(self.matched_up_participants_list[self.round_index][1])
                self.round_index += 1
        else:
            if if_win:
                self.winners.append(self.matched_up_participants_list[self.round_index][0])
                self.round_index += 1
            else:
                self.winners.append(self.matched_up_participants_list[self.round_index][1])
                self.round_index += 1

    def stop_1v1(self, srv):
        global glob_tournaments
        if next((x for x in glob_tournaments if x.guild == srv.message.guild.id), None):
            for x in glob_tournaments:
                if srv.message.guild.id == x.guild:
                    glob_tournaments.pop(glob_tournaments.index(x))
                    break

    def init_text(self):
        self.matched_up_text_with_wins = ''
        if self.round_index < len(self.matched_up_participants_list):
            for x in range(len(self.matched_up_participants_text_list)):
                if x == self.round_index:
                    self.matched_up_text_with_wins += '\n' + str(
                        self.matched_up_participants_text_list[x]) + '     Current match'
                elif x - 1 == self.round_index:
                    self.matched_up_text_with_wins += '\n' + str(
                        self.matched_up_participants_text_list[x]) + '     Next match'
                elif x < self.round_index:
                    self.matched_up_text_with_wins += '\n' + str(
                        self.matched_up_participants_text_list[x]) + f'     Winner - **{self.winners[x]}**'
            self.current_round = self.matched_up_participants_text_list[self.round_index]
        else:
            for x in range(len(self.matched_up_participants_text_list)):
                self.matched_up_text_with_wins += '\n' + str(
                    self.matched_up_participants_text_list[x]) + f'     Winner - **{self.winners[x]}**'
            self.current_round = ''

    def tournament_end_check(self, ctx):
        if self.round_index >= len(self.matched_up_participants_list):
            self.stop_1v1(ctx)

    def checks(self, guild):
        self.init_text()


glob_tournaments = []
tournament_logs = []

bot_token = pickle.load(open('Requiem 2.0 - Token', 'rb'))
member_list = []
log = []
suggestions = []
anime_list = []
anim_test = []
forbidden_animes = ['Boku No Pico']
sorted_anime_list = [[], [], [], []]
s_tier_animes = sorted_anime_list[0]
a_tier_animes = sorted_anime_list[1]
b_tier_animes = sorted_anime_list[2]
c_tier_animes = sorted_anime_list[3]

auto_mod_data = [[], [], []]

xp_data_all = [[], [], [], []]

try:
    log = pickle.load(open("Requiem 2.0 - Log", "rb"))
except FileNotFoundError:
    pickle.dump(log, open("Requiem 2.0 - Log", "wb"))

try:
    suggestions = pickle.load(open("Requiem 2.0 - Suggestions", "rb"))
except FileNotFoundError:
    pickle.dump(suggestions, open("Requiem 2.0 - Suggestions", "wb"))

try:
    anime_list = pickle.load(open("Requiem 2.0 - Data", "rb"))[0]
    forbidden_animes = pickle.load(open("Requiem 2.0 - Data", "rb"))[1]
    sorted_anime_list = pickle.load(open("Requiem 2.0 - Data", "rb"))[2]
    xp_data_all = pickle.load(open('Requiem 2.0 - Data', 'rb'))[3]
    auto_mod_data = pickle.load(open('Requiem 2.0 - Data', 'rb'))[4]
    tournament_logs = pickle.load(open('Requiem 2.0 - Data', 'rb'))[5]
except FileNotFoundError:
    pickle.dump([[], ['Boku No Pico'], [[], [], [], []], [[], [], [], []], [[], []], []],
                open('Requiem 2.0 - Data', 'wb'))

global_id = xp_data_all[0]
global_exp = xp_data_all[1]
allowed_channels = xp_data_all[2]

sfw_channels = auto_mod_data[0]
banned_words = auto_mod_data[1]


def save_data():
    pickle.dump([anime_list, forbidden_animes, sorted_anime_list, [global_id, global_exp, allowed_channels],[sfw_channels, banned_words], tournament_logs], open(
        'Requiem 2.0 - Data', 'wb'))

client = commands.Bot(command_prefix='.')
common, uncommon, rare, legendary, mythical = 50, 50, 50, 50, 50
ss = [["Copper shortsword", 5, 10, 0, 1, 100, 0, common], ["Tin shortsword", 5, 11, 0, 1, 100, 0, common],
      ["Iron shortsword", 6, 12, 0, 1, 100, 0, common],
      ["Lead shortsword", 6, 13, 0, 1, 100, 0, uncommon], ["Silver shortsword", 6, 13, 0, 1, 100, 0, uncommon],
      ["Tungsten shortsword", 7, 14, 0, 1, 100, 0, uncommon], ["Crimson shortsword", 7, 14, 0, 1, 100, 0, rare],
      ["Gold shortsword", 8, 14, 0, 1, 100, 0, rare], ["Platinum shortsword", 9, 15, 0, 1, 100, 0, legendary],
      ["Katana", 10, 20, 0, 1, 200, 0, legendary]]
bs = [["Iron broadsword", 0, 7, 0, 1, 10, 0, uncommon], ["Lead broadsword", 0, 7, 0, 1, 10, 0, uncommon],
      ["Silver broadsword", 0, 7, 0, 1, 10, 0, uncommon],
      ["Tungsten broadsword", 0, 8, 0, 1, 10, 0, uncommon], ["Crimson broadsword", 0, 8, 0, 1, 10, 0, rare],
      ["Gold broadsword", 0, 10, 0, 1, 10, 0, rare],
      ["Platinum broadsword", 0, 12, 0, 1, 10, 0, legendary]]
sp = [["Spear", 10, 15, 0, 1, 50, 0, common], ["Trident", 6, 8, 2, 3, 75, 0, rare],
      ["Glaive", 15, 20, 0, 1, 40, 0, rare]]
st = [["Amethyst staff", 20, 25, 20, 1, 70, 0, common], ["Topaz staff", 20, 25, 20, 1, 70, 1, common],
      ["Sapphire staff", 20, 25, 20, 1, 70, 0, common], ["Emerald staff", 20, 25, 20, 1, 70, 0, uncommon],
      ["Ruby staff", 25, 27, 20, 1, 70, 0, uncommon], ["Diamond staff", 25, 27, 20, 5, 70, 1, legendary],
      ["Amber staff", 20, 25, 20, 1, 70, 2, common]]
mg = [["Last prism", 25, 40, 75, 7, 25, 2, mythical], ["Star Wrath", 10, 15, 5, 3, 10, 2, mythical],
      ["Phantasm", 20, 30, 10, 1, 20, 1, mythical], ["Meowmere", 50, 70, 0, 4, 10, 4, mythical],
      ["Celebration MK.2", 7, 13, 5, 3, 10, 2, mythical], ["Solar Eruption", 30, 60, 0, 20, 25, 2, mythical],
      ["Holy Water", 1000000, 1000000, 100, 1, 5, 3, mythical]]
weapons = [ss, bs, sp, st, mg]
global_chest = []


# Regular functions -----------------------------


def is_retard_server(server_thing):
    if server_thing.guild.id == 500614426051739669:
        return True


def get_time():
    return time.strftime('%c', time.localtime())


def add_to_log(server_thing, command_name, fetched_user):
    appropriate_white_space = 38 - len(str(fetched_user))
    log.append(
        str(str(fetched_user) + (' ' * abs(appropriate_white_space)) + str(command_name) + " " + str(get_time())))
    pickle.dump(log, open("Requiem 2.0 - Log", "wb"))
    # await client.fetch_user(server_thing.message.author.id)


# Regular functions -----------------------------

# Bot stats -------------------------------------

@client.event
async def on_ready():
    print('Bot is online')


@client.command(brief='its in the name', pass_context=True)
async def ping(ctx):
    add_to_log(ctx, '  PING', await client.fetch_user(ctx.message.author.id))
    await ctx.send(f'Ping : {round((client.latency * 1000))}ms')


@client.command(hidden=True, pass_context=True)
async def ass_n_tiddi(ctx):
    add_to_log(ctx, 'S_N_TT', await client.fetch_user(ctx.message.author.id))
    await ctx.send(f'ASS AND TIDDIES - Raph_Li68')


@client.command(pass_context=True, brief='Sends suggestions to the creator of the bot.(asian_nerd#1090)',
                description='Sends suggestions to the creator of the bot.(asian_nerd#1090)\nFormat:\n.suggest '
                            '{suggestion here}')
async def suggest(ctx, *args):
    add_to_log(ctx, 'SGGEST', await client.fetch_user(ctx.message.author.id))
    suggestions.append((str(await client.fetch_user(ctx.message.author.id))) + ' - ' + str(' '.join(args)))
    pickle.dump(suggestions, open('Requiem 2.0 - Suggestions', 'wb'))
    await ctx.send(f'Your suggestion ,"{" ".join(args)}", has been recorded.')


@client.command(pass_context=True, brief='Sends the Suggestions file as a text file.',
                description='Sends the Suggestions file as a text file.\nIgnore the weird symbols and stuff. Those '
                            'are artifacts of byte to utf=8 conversion. FYI This does not contain child porn. TRUST '
                            'ME')
async def get_suggestions(ctx):
    add_to_log(ctx, 'SLOGFL', await client.fetch_user(ctx.message.author.id))
    with open('Requiem 2.0 - Suggestions', 'rb', ) as fp:
        await ctx.send(file=discord.File(fp, 'Requiem 2.0 - Suggestions.txt'))


# Bot stats -------------------------------------

# Light commands --------------------------------


@client.command(pass_context=True, brief='Out of sight',
                description='Out of sight. Use this to erase the weird fucking '
                            'jotaro hentai you '
                            'just searched up')
async def oos(ctx):
    add_to_log(ctx, '   OOS', await client.fetch_user(ctx.message.author.id))
    await ctx.send(
        '‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎'
        '‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n'
        '‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n'
        '‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎‎\n‎')


@client.command(pass_context=True, brief='Randomizes order of input',
                description='Randomizes the order of the input. {object},{object}')
async def shuffle(ctx, args):
    add_to_log(ctx, '  SHFL', await client.fetch_user(ctx.message.author.id))
    elements = args.split(',')
    random.shuffle(elements)
    '\n'.join(elements)
    await ctx.send('\n'.join(elements))


@client.command(pass_context=True, brief='Picks one out of the arguments',
                description='Picks one out of the arguments.\nFormat:\n{object},{object}')
async def pick(ctx, *args):
    await ctx.send(random.choice(args))


@client.command(pass_context=True, brief='Sends a random number from the range given',
                description='Sends a random number from the range given.\nFormat:\n.rand {minimum} {maximum}')
async def rand(ctx, *args):
    randmin = args[0]
    randmax = args[1]
    try:
        int(randmin)
    except ValueError:
        await ctx.send('The first argument is not an integer.')
    try:
        int(randmax)
    except ValueError:
        await ctx.send('The second argument is not an integer.')
    await ctx.send(random.randint(int(randmin), int(randmax)))


@client.command(pass_context=True)
async def retardify(ctx, *args):
    add_to_log(ctx, 'RTRDFY', await client.fetch_user(ctx.message.author.id))
    retarded = ''
    retard_words = ' '.join(args)
    i = True  # capitalize
    for char in retard_words:
        if i:
            retarded += char.upper()
        else:
            retarded += char.lower()
        if char != ' ':
            i = not i
    await ctx.send(retarded)


@client.command(pass_context=True)
async def onelinify(ctx, args):
    nothing = '\\' + 'n'
    await ctx.send('exec("' + nothing.join(args.split("\n")) + '")')


# Light commands --------------------------------

# Game stuff

@client.command(pass_context=True, brief='Starts a tournament',
                description='Starts a tournament.\nFormat:\n.start_tournament {participant 1} {participant 2} {participant 3} {participant 4}')
@has_any_role('Bot Doctor', 'Admin')
async def start_tournament(ctx, *args):
    add_to_log(ctx,'STRTTR',await client.fetch_user(ctx.message.author.id))
    newline = '\n  -'
    args = list(args)
    for x in glob_tournaments:
        x.checks(ctx)
    if int(len(args) / 2):
        if len(glob_tournaments) != 0:
            for y in glob_tournaments:
                if ctx.message.guild.id != y.guild:
                    glob_tournaments.append(Tournaments(ctx.message.guild.id, list(args), ctx.message.author.id))
                    await ctx.send(
                        f'A tournament has been started.\nParticipants\n{newline+(newline.join(args))}\nMatches\n{y.matched_up_text_with_wins}')
                else:
                    await ctx.send('There is already an ongoing tournament in this server.')
        else:
            glob_tournaments.append(Tournaments(ctx.message.guild.id, args, ctx.message.author.id))
    else:
        await ctx.send(f'The amount of participants are not even. Tournament will not be started.')


@client.command(brief='Sends current tournament information',
                description='Sends current tournament information.\n{Match index}. {Contestant 1} VS {Contestant 2}')
async def rounds(ctx):
    for x in glob_tournaments:
        if x.guild == ctx.message.guild.id:
            for x in glob_tournaments:
                x.checks(ctx)
            for x in glob_tournaments:
                if ctx.message.guild.id == x.guild:
                    await ctx.send(f'**Current Tournament**\n{x.matched_up_text_with_wins}')
        else:
            await ctx.send('There isnt currently a tournament in this server.')
    if len(glob_tournaments) == 0:
        await ctx.send('There isnt currently a tournament in this server.')


@client.command(brief='Sets the result of the round [W/L]',
                description='Sets the results of the round [W/L].Only Bot Doctors and admins can use this.')
@has_any_role('Bot Doctor', 'Admin')
async def round_result(ctx, args):
    add_to_log(ctx,'RNDRST',await client.fetch_user(ctx.message.author.id))
    args = args.lower()
    newline = '\n'
    if next((x for x in glob_tournaments if x.guild == ctx.message.guild.id), None):
        for x in glob_tournaments:
            x.checks(ctx)
            if x.guild == ctx.message.guild.id:
                if args in ['w', 'l']:
                    if args in ['w']:
                        await ctx.send(f'**Winner -- {x.matched_up_participants_list[x.round_index][0]}**')
                        x.set_round_result(True)
                    elif args in ['l']:
                        await ctx.send(f'**Winner -- {x.matched_up_participants_list[x.round_index][1]}**')
                        x.set_round_result(False)
                else:
                    await ctx.send('Arguments insufficient or incorrect.')
    else:
        await ctx.send('There isnt currently a tournament in this server.')
    for x in glob_tournaments:
        if ctx.message.guild.id == x.guild:
            if x.round_index >= len(x.matched_up_participants_list):
                x.init_text()
                await ctx.send(
                    f'**The Tournament has ended**\n\n**Tournament Starter**\n<@{x.tmnt_starter_id}>\n**Participants**\n{newline.join(x.p_text_all)}\n**Winners**\n{newline.join(x.winners)}\n**Matches**\n{x.matched_up_text_with_wins}')
                tournament_logs.append([x.guild, x.tmnt_starter_id, x.participants, x.matched_up_text_with_wins,
                                        time.strftime('%c', time.localtime())])
                save_data()
                glob_tournaments.pop(glob_tournaments.index(x))
                break


@client.command(brief='Stops the tournament - Only for the tournament starter',
                description='Stops the tournament - Only for the tournament starter.')
async def stop_tournament(ctx):
    if next((x for x in glob_tournaments if x.guild == ctx.message.guild.id), None):
        for x in glob_tournaments:
            if ctx.message.guild.id == x.guild:
                if ctx.message.author.id == x.tmnt_starter_id:
                    glob_tournaments.pop(glob_tournaments.index(x))
                else:
                    await ctx.send(f'You are not the tournament starter. You are not allowed to stop the tournament.')
    else:
        await ctx.send('There isnt currently a tournament in this server.')


@client.command(pass_context=True, hidden=True)
@has_role('Bot Doctor')
async def admin_stop_tournament(ctx):
    await ctx.message.delete()
    if next((x for x in glob_tournaments if x.guild == ctx.message.guild.id), None):
        for x in glob_tournaments:
            if ctx.message.guild.id == x.guild:
                if ctx.message.author.id == x.tmnt_starter_id:
                    glob_tournaments.pop(glob_tournaments.index(x))


# split from the tourney commands

@client.command(pass_context=True, brief='Generates a random weapon.',
                description='Adds a random weapon to the global chest (.chest)')
async def loot(ctx, *args):
    add_to_log(ctx, '  LOOT', await client.fetch_user(ctx.message.author.id))
    weapon_index = random.randint(0, len(weapons))
    weapon_class_index = random.randint(0, ((len(weapons[weapon_index - 1])) - 1))
    global_chest.append(weapons[weapon_index - 1][weapon_class_index][0])
    await ctx.send(weapons[weapon_index - 1][weapon_class_index][0])


@client.command(pass_context=True, hidden=True)
async def loot_table(ctx):
    add_to_log(ctx, 'LT_TBL', await client.fetch_user(ctx.message.author.id))
    await ctx.send(weapons)


@client.command(pass_context=True, brief='Shows the global chest',
                description='Shows all the loot collected from .loot.')
async def chest(ctx):
    add_to_log(ctx, '  CHST', await client.fetch_user(ctx.message.author.id))
    await ctx.send(global_chest)


# Game stuff ------------------------------------

# Bot control -----------------------------------

@client.command(pass_context=True, hidden=True)
async def cred(ctx):
    add_to_log(ctx, '  CRED', await client.fetch_user(ctx.message.author.id))
    await ctx.send(' @asian_nerd#1090 is my father')


@client.command(pass_context=True, hidden=True)
@has_role("Bot Doctor")
async def shut_down(ctx):
    add_to_log(ctx, ' SH_DN', await client.fetch_user(ctx.message.author.id))
    await ctx.send(f'{ctx.message.author.name} has shut me down.')
    print(ctx.message.author.name)
    await client.close()


@client.command(pass_context=True, brief="Changes the bot's status",
                description="Changes the bot description.\nFormat:\ng - Game\nl - "
                            "Listening\ns - Streaming\nw - Watching")
async def change_pres(ctx, *args):
    add_to_log(ctx, 'STATUS', await client.fetch_user(ctx.message.author.id))
    acts = ['g', 'l', 's', 'w']
    wanted_act = args[0]
    wanted_subject = args[1]
    if wanted_act == acts[2]:
        if len(args) >= 3:
            wanted_link = args[2]
        else:
            wanted_link = ''
            await ctx.send(
                f'Arguments insufficient or incorrect     - Streaming status needs to be provided with a url')
    else:
        wanted_link = ''
    if wanted_act in acts:
        if wanted_act == acts[0]:
            await client.change_presence(activity=discord.Game(name=wanted_subject))
            await ctx.send(f'Activity set to **Playing {wanted_subject}**')
        elif wanted_act == acts[1]:
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening, name=wanted_subject))
            await ctx.send(f'Activity set to **Listening to {wanted_subject}**')
        elif wanted_act == acts[2]:
            await client.change_presence(activity=discord.Streaming(name=wanted_subject, url=wanted_link))
            await ctx.send(f'Activity set to **Streaming {wanted_subject} at {wanted_link}**')
        elif wanted_act == acts[3]:
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=wanted_subject))
            await ctx.send(f'Activity set to **Watching {wanted_subject}**')
    else:
        await ctx.send(f'Arguments insufficient or incorrect   -{args, wanted_act, wanted_subject}')


@client.command(pass_context=True, hidden=True)
@has_role('Bot Doctor')
async def change_stat(ctx, args):
    if args in ['do', 'on', 'id', 'in']:
        if args == 'do':
            await client.change_presence(status=discord.Status.do_not_disturb)
        if args == 'on':
            await client.change_presence(status=discord.Status.online)
        if args == 'id':
            await client.change_presence(status=discord.Status.idle)
        if args == 'in':
            await client.change_presence(status=discord.Status.invisible)
    else:
        await ctx.send('arg not in activity list')


@client.command(pass_context=True, hidden=True)
async def get_log(ctx):
    if len(log) > 0:
        await ctx.send((str('```') + '\n'.join(log[-27::]) + str('```')))
    else:
        await ctx.send('``` ```')


@client.command(pass_context=True, hidden=True)
async def get_log_file(ctx):
    add_to_log(ctx, 'GT_LGF', await client.fetch_user(ctx.message.author.id))
    with open('Requiem 2.0 - Log', 'rb', ) as fp:
        await ctx.send(file=discord.File(fp, 'Requiem 2.0 - Log.txt'))


@client.command(pass_context=True, hidden=True)
async def get_log_console(ctx):
    add_to_log(ctx, 'GT_LGC', await client.fetch_user(ctx.message.author.id))
    print('\n'.join(pickle.load(open('Requiem 2.0 - Log', 'rb'))))


# Anime -----------------------------------------

@client.command(brief='Adds Anime to Anime suggestions.(ONLY FOR THE RETARDS SERVER)',
                description='Adds Anime to Anime suggestions.(ONLY FOR THE RETARDS SERVER)\nFormat:\n.ads {anime name}')
async def ads(ctx, *args):
    add_to_log(ctx, 'ANIADD', await client.fetch_user(ctx.message.author.id))
    args = list(args)
    for x in range(len(args)):
        args[x] = args[x].capitalize()
    if is_retard_server(ctx):
        if (str(' '.join(args)) not in anime_list) and (str(' '.join(args)) not in forbidden_animes):
            anime_list.append(str(' '.join(args)))
            await ctx.send('Your anime ,"' + ' '.join(args) + '", has been successfully recorded.')
        else:
            if str(' '.join(args)) not in forbidden_animes:
                await ctx.send(
                    'Your anime ,"' + ' '.join(args) + '", has not been accepted. It is already in the anime list')
            else:
                await ctx.send(
                    'Your anime ,"' + ' '.join(args) + '", has not been recorded. Fuck you, you piece of shit.')
    else:
        await ctx.send('Sorry this command can only be used by the "Retards" server.')
    pickle.dump(anime_list, open('Requiem 2.0 - Animes', 'wb'))
    save_data()


@client.command(hidden=True)
@has_role("Bot Doctor")
async def forbid_anime(ctx, *args):
    add_to_log(ctx, 'GTFANI', await client.fetch_user(ctx.message.author.id))
    args = list(args)
    for x in range(len(args)):
        args[x] = args[x].capitalize()
    forbidden_animes.append(str(' '.join(args)))
    await ctx.send('The forbidden anime,"' + str(' '.join(args)) + '", has been successfully recorded.')
    save_data()
    pickle.dump(forbidden_animes, open("Requiem 2.0 - Forbidden Animes", "wb"))


@client.command(hidden=True, pass_context=True)
async def get_forbidden_animes(ctx):
    if len(str(forbidden_animes)) < 2000:
        await ctx.send('\n'.join(forbidden_animes))
    else:
        await ctx.send('Sorry the forbidden anime list is too long. Heres the file instead.')
        with open('Requiem 2.0 - Forbidden Animes') as fp:
            await ctx.send(file=discord.File(fp, 'Requiem 2.0 - Forbidden Animes.txt'))


@client.command(hidden=True)
async def get_animes(ctx):
    add_to_log(ctx, 'GETANI', await client.fetch_user(ctx.message.author.id))
    if len(str(anime_list)) < 2000:
        anime_list.sort()
        await ctx.send('**Anime list : Count ' + str(len(anime_list)) + '**\n```' + '\n'.join(anime_list) + '```')
    else:
        await ctx.send(
            'The anime list is too long. Please refer to the file instead.')


# sorting

@client.command(hidden=True, brief='Adds the selected anime to the tier.', description='.st {anime name here}')
async def st(ctx, *args):
    global sorted_anime_list
    if is_retard_server(ctx):
        args = list(args)
        for x in range(len(args)):
            args[x] = args[x].capitalize()
        if ' '.join(args) in anime_list:
            s_tier_animes.append(' '.join(args))
            sorted_anime_list = [s_tier_animes, a_tier_animes, b_tier_animes, c_tier_animes]
            pickle.dump(sorted_anime_list, open("Requiem 2.0 - Sorted Animes", "wb"))
            save_data()
        else:
            await ctx.send('The anime ,"' + str(' '.join(args)) + '", was not in the anime list.')


@client.command(hidden=True, brief='Adds the selected anime to the tier.', description='.at {anime name here}')
async def at(ctx, *args):
    global sorted_anime_list
    if is_retard_server(ctx):
        args = list(args)
        for x in range(len(args)):
            args[x] = args[x].capitalize()
        if ' '.join(args) in anime_list:
            a_tier_animes.append(' '.join(args))
            sorted_anime_list = [s_tier_animes, a_tier_animes, b_tier_animes, c_tier_animes]
            pickle.dump(sorted_anime_list, open("Requiem 2.0 - Sorted Animes", "wb"))
            save_data()
        else:
            await ctx.send('The anime ,"' + str(' '.join(args)) + '", was not in the anime list.')


@client.command(hidden=True, brief='Adds the selected anime to the tier.', description='.bt {anime name here}')
async def bt(ctx, *args):
    global sorted_anime_list
    if is_retard_server(ctx):
        args = list(args)
        for x in range(len(args)):
            args[x] = args[x].capitalize()
        if ' '.join(args) in anime_list:
            b_tier_animes.append(' '.join(args))
            sorted_anime_list = [s_tier_animes, a_tier_animes, b_tier_animes, c_tier_animes]
            pickle.dump(sorted_anime_list, open("Requiem 2.0 - Sorted Animes", "wb"))
            save_data()
        else:
            await ctx.send('The anime ,"' + str(' '.join(args)) + '", was not in the anime list.')


@client.command(hidden=True, brief='Adds the selected anime to the tier.', description='.ct {anime name here}')
async def ct(ctx, *args):
    global sorted_anime_list
    if is_retard_server(ctx):
        args = list(args)
        for x in range(len(args)):
            args[x] = args[x].capitalize()
        if ' '.join(args) in anime_list:
            c_tier_animes.append(' '.join(args))
            sorted_anime_list = [s_tier_animes, a_tier_animes, b_tier_animes, c_tier_animes]
            pickle.dump(sorted_anime_list, open("Requiem 2.0 - Sorted Animes", "wb"))
            save_data()
        else:
            await ctx.send('The anime ,"' + str(' '.join(args)) + '", was not in the anime list.')


@client.command(hidden=True)
async def get_animes_sorted(ctx):
    add_to_log(ctx, 'GTANIS', await client.fetch_user(ctx.message.author.id))
    await ctx.send(str('**S Tier Animes**\n```') + '\n'.join(sorted_anime_list[0]) + str('```'))
    await ctx.send(str('**A Tier Animes**\n```') + '\n'.join(sorted_anime_list[1]) + str('```'))
    await ctx.send(str('**B Tier Animes**\n```') + '\n'.join(sorted_anime_list[2]) + str('```'))
    await ctx.send(str('**C Tier Animes**\n```') + '\n'.join(sorted_anime_list[3]) + str('```'))


# @client.command(hidden=True)
# @has_role('Bot Doctor')
# async def dont(ctx, args):
#     global anim_test
#     if is_retard_server(ctx):
#         args_capped = []
#         args = args.split('\n')
#         for y in range(len(args)):
#             args_capped.append(' '.join([word.capitalize() for word in args[y].split(' ')]))
#         args_capped = '\n'.join(args_capped)
#
#         for x in range(len(args_capped.split('\n'))):
#             if args_capped.split('\n')[x] not in anim_test:
#                 anim_test.append(str(args_capped.split('\n')[x]))
#         print(anim_test)

# Anime -----------------------------------------

# XP --------------------------------------------

@client.event
async def on_message(message):
    global global_id, global_exp, allowed_channels, xp_data_all
    if message.channel.id in sfw_channels:
        if any(word in message.content for word in banned_words):
            await message.delete()
    if not message.author.bot:
        if message.author.id not in global_id:
            global_id.append(message.author.id)
            global_exp.append(Exp())

        selected_user_index = global_id.index(message.author.id)
        global_exp[selected_user_index].add_exp(message.content)

        global_exp[selected_user_index].check_level_up(message, selected_user_index)

        if global_exp[selected_user_index].send_chat_level_up():
            if message.channel.id in allowed_channels:
                await message.channel.send(
                    f'<@{message.author.id}> has leveled up!\n{global_exp[selected_user_index].level - 1} --> {global_exp[selected_user_index].level}')

        if message.content == 'get_lvl':
            await message.channel.send(
                f'{global_exp[global_id.index(message.author.id)].current_exp}/{global_exp[global_id.index(message.author.id)].required_level_exp}: EXP\n{global_exp[global_id.index(message.author.id)].level} : LVL')
        if message.content == 'glob_rank':
            apostrosphe = "'"
            global_rankings_text = ''
            global_id_sorted = []
            # ([y for _, y in sorted(zip(sorted(global_exp,key=lambda x:x.total_exp), global_id))])[0]
            for y in sorted(zip(global_id, global_exp), key=lambda x: getattr(x[1], 'total_exp'), reverse=True):
                global_id_sorted.append(y[0])
            for x in range(len(global_exp[:32])):
                # Not using fstrings here cos idk how to change heroku's python versions
                global_rankings_text += (
                    '\n'+(str(x + 1).rjust(2, " "))+'. LVL:'+(sorted(global_exp, key=lambda x: x.total_exp, reverse=True)[x].level)+' EXP:'+(str(sorted(global_exp, key=lambda x: x.total_exp, reverse=True)[x].total_exp).rjust(6, apostrosphe))+str(await client.fetch_user(global_id_sorted[x])))
            await message.channel.send(
                f'**Global Rankings** ```' + global_rankings_text + '```' + '_This is just the top 32 because of discords character limit._')

        xp_data_all = [global_id, global_exp, allowed_channels]
        save_data()
    await client.process_commands(message)


@client.command(hidden=True, pass_context=True)
@has_role('Bot Doctor')
async def exp_allow_channel(ctx):
    add_to_log(ctx, 'FBDCHL', await client.fetch_user(ctx.message.author.id))
    global xp_data_all
    if ctx.message.channel.id not in allowed_channels:
        allowed_channels.append(ctx.message.channel.id)
        await ctx.message.channel.send(
            f'The channel "#{ctx.message.channel}" has been added to the allowed channels.')
    else:
        await ctx.send('This channel is already in the allowed channels.')
    xp_data_all = [global_id, global_exp, allowed_channels]
    pickle.dump(xp_data_all, open('Requiem 2.0 - XP', 'wb'))
    save_data()


# XP --------------------------------------------

# Study Group -----------------------------------


@client.command(hidden=True)
async def register(ctx):
    if ctx.message.guild.id == 681866342189891608:
        if ctx.message.channel.id == 688069390402715678:
            await ctx.message.author.add_roles(ctx.guild.get_role(688068168224079988))
            await ctx.send(f'<@{ctx.message.author.id}> is now registered for `#off-topic-and-memes`.')


@client.command(hidden=True)
@has_role('moldy abortion')
async def leave_off_topic(ctx):
    if ctx.message.guild.id == 681866342189891608:
        if ctx.message.channel.id in [681866657555415108, 743137400204820590, 716794375920812103]:
            await ctx.message.author.remove_roles(ctx.guild.get_role(688068168224079988))
            await ctx.send(f'<@{ctx.message.author.id}> has removed their off-topic subscription.')


# Study Group -----------------------------------

# Auto - Moderation -----------------------------


@client.command(brief='Deletes messages',
                description='Deletes messages.\nOnly works for those with the manage messagse permission.\nFormat:\n.phurge {amount of messages to delete}')
@has_permissions(manage_messages=True)
async def phurge(ctx, *args):
    add_to_log(ctx, 'PHURGE', await client.fetch_user(ctx.message.author.id))
    if type(args[0]) == str:
        args = int(args[0]) + 1
        await ctx.message.channel.purge(limit=args)
    else:
        await ctx.send(f'Purge amount argument incorrect.')


@client.command(pass_context=True)
@has_permissions(manage_messages=True)
async def sfw_channel_add(ctx):
    add_to_log(ctx, 'SFWADD', await client.fetch_user(ctx.message.author.id))
    if ctx.message.channel.id not in sfw_channels:
        sfw_channels.append(ctx.message.channel.id)
        await ctx.send(f'The channel "#{ctx.message.channel}" has swears now banned.')
    else:
        await ctx.send(f'"#{ctx.message.channel}" has swears already banned.')
    save_data()


@client.command(pass_context=True)
@has_permissions(manage_messages=True)
async def sfw_channel_remove(ctx):
    add_to_log(ctx, 'SFWRMV', await client.fetch_user(ctx.message.author.id))
    if ctx.message.channel.id in sfw_channels:
        sfw_channels.remove(ctx.message.channel.id)
        await ctx.send(f'The channel "#{ctx.message.channel}" has swears now allowed.')
    else:
        await ctx.send(f'#"{ctx.message.channel}" has swears already allowed.')
    save_data()


@client.command(pass_context=True, brief='Removes banned words',
                description='Removes banned words. Only works for those with the Bot Doctor role.\nFormat:\n'
                            '.banned_words_remove {word} {word}',hidden=True)
@has_role('Bot Doctor')
async def banned_word_remove(ctx, *args):
    global banned_words
    add_to_log(ctx, 'BNWRMV', await client.fetch_user(ctx.message.author.id))
    list(args)
    for x in range(len(args)):
        if args[x] in banned_words:
            banned_words[x].pop()
    await ctx.send(f'The words, {",".join(args)} have been unbanned.')


@client.command(pass_context=True, brief='Adds banned words',
                description='Adds banned words. Only works for those with the Bot Doctor role.\nFormat:\n'
                            '.banned_words_add {word} {word}',hidden=True)
@has_role('Bot Doctor')
async def banned_words_add(ctx, *args):
    global banned_words
    add_to_log(ctx, 'BNWADD', await client.fetch_user(ctx.message.author.id))
    list(args)
    for x in range(len(args)):
        if args[x] not in banned_words:
            banned_words.append(args[x])
    await ctx.send(f'The words, {",".join(args)} have been banned.')


# Auto - Moderation -----------------------------


client.run(bot_token)
