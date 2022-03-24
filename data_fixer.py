"""
used to fix json data whenever a new update is released
"""

import json

final = {}

with open('Jaden2GM/users.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    for x in data.items():
        final[x[0]] = x[1]
        final[x[0]]['inventory'] = {
            "consumable": {},
            "equipment": {}
        }

with open('Jaden2GM/users.json', 'w', encoding='utf-8') as file:
    json.dump(final, file, ensure_ascii=False, indent=4)

