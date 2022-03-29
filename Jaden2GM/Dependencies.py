import json

with open('data.json', 'r') as d:
    data_file = json.load(d)

token = ''

help_info = {}

command_prefix = ''
master_id = 0
default_embed_colour = 0
success_embed_colour = 0
error_embed_colour = 0
battle_embed_colour = 0

quests_per_page = 0


def init():
    global token, command_prefix, master_id, default_embed_colour, success_embed_colour, error_embed_colour,\
        battle_embed_colour, quests_per_page, help_info
    with open('Data/token.json', 'r') as t:
        token = json.load(t)['token']

    with open('help.json', 'r') as file:
        help_info = json.load(file)

    command_prefix = data_file['prefix']
    master_id = int(data_file['master_id'])
    default_embed_colour = int(data_file['default_embed_colour'])
    success_embed_colour = int(data_file['success_embed_colour'])
    error_embed_colour = int(data_file['error_embed_colour'])
    battle_embed_colour = int(data_file['battle_embed_colour'])

    quests_per_page = int(data_file['quests_per_page'])
