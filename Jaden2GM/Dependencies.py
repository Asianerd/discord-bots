import json

data_file = json.load(open('data.json', 'r'))
token = ''

command_prefix = ''
master_id = 0
default_embed_colour = 0


def init():
    global token, command_prefix, master_id, default_embed_colour
    token = json.load(open('token.json', 'r'))['token']

    command_prefix = data_file['prefix']
    master_id = int(data_file['master_id'])
    default_embed_colour = int(data_file['default_embed_colour'])
