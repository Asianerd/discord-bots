from PIL import Image
import os

prefixes = ['meth', 'eth', 'prop', 'but', 'pent', 'hex', 'hept', 'oct', 'non', 'dec']
suffixes = ['ane', 'ene', 'yne', 'anol', 'anoic', 'anoate']
subscripts = '₀₁₂₃₄₅₆₇₈₉'
# ⁰¹²³⁴⁵⁶⁷⁸⁹
# ₀₁₂₃₄₅₆₇₈₉
# ⁺⁻⁼⁽⁾ⁿ ₊₋ ₘₙ

segment_width = 144
segment_height = 640

image_library = {}

def initialize():
    global image_library
    image_library = {}
    for x in ['.'.join(i.split('.')[:-1]) for i in os.listdir("chemistry_assets/media")]:
        #image_library[x] = Image.open(f'chemistry_assets/media/{x}.png')
        image = Image.open(f'chemistry_assets/media/{x}.png')
        image_library[x] = [
            image,
            int(image.width / segment_width)
        ]

def fix_input(name: str):
    if not name:
        return name
    name = name.strip().split()[0]
    c, s, l = parse_suffix_prefix(name)
    if (c < 0) or (s < 0):
        return 'invalid'
    if l != 0:
        return f'{prefixes[c]}-{l}-{suffixes[s]}'
    else:
        return prefixes[c] + suffixes[s]    

def parse_suffix_prefix(name: str):
    """
    returns the carbon count(-1), series(-1) and carbon location
    eg:
        - methane -> carbon = 0, series = 0
    """
    if name:
        name = name.strip().split()[0]
    parsed_int = 1
    if name.count('-') >= 2:
        i = name.index('-')
        raw_location = name[(i + 1):].split('-')[0]
        try:
            parsed_int = int(raw_location)
        except Exception as e:
            pass
    c = [index for index, i in enumerate(prefixes) if name.startswith(i)][0] if [index for index, i in enumerate(prefixes) if name.startswith(i)] else -1
    if not (parsed_int in range(1, c + 2)):
        parsed_int = 1
    # highest = c + 2
    # if (highest - parsed_int) < parsed_int:
    #     parsed_int = highest - parsed_int
    return [
        c,
        [index for index, i in enumerate(suffixes) if name.endswith(i)][0] if [index for index, i in enumerate(suffixes) if name.endswith(i)] else -1,
        parsed_int
    ]

def hydrocarbon(name: str):
    """
    mepb
        - meth
        - eth
        - prop
        - but
        - pent
        - hex
        - hept
        - oct
        - non
        - dec

    aeyo
        - ane
        - ene
        - yne
        - ol
        - oic
        - oate

    functional group
        - alkane
        - alkene
        - alkyne
        - alcohol
        - carboxylic acid
        - ester
    """
    if name:
        name = name.strip().split()[0]
    carbon, series, pos = parse_suffix_prefix(name)
    if (carbon + series) == -2:
        return False
    return {
        # ⁰¹²³⁴⁵⁶⁷⁸⁹
        # ₀₁₂₃₄₅₆₇₈₉
        # ⁺⁻⁼⁽⁾ⁿ ₊₋ ₘₙ
        'carbon': carbon + 1,
        'h_series': 'alkane,alkene,alkyne,alcohol,carboxylic acid,ester'.split(',')[series].capitalize(),
        'f_group': 'Single bond between carbon atoms,Double bond between carbon atoms,Triple bond between carbon atom,Hydroxyl,Carboxyl,Carboxylate'.split(',')[series],
        'o_type': 'Saturated hydrocarbon,Unsaturated hydrocarbon,Unsaturated hydrocarbon,Non hydrocarbon,Non hydrocarbon,Non hydrocarbon'.split(',')[series],
        'general_formula': [
            ["CₙH₂ₙ₊₂", "n=1,2,3,..."],
            ["CₙH₂ₙ", "n=2,3,4,..."],
            ["CₙH₂ₙ₋₂", "n=2,3,4,..."],
            ["CₙH₂ₙ₊₁OH", "n=1,2,3,..."],
            ["CₙH₂ₙ₊₁COOH", "n=0,1,2,..."],
            ["CₘH₂ₘ₊₁COOCₙH₂ₙ₊₁", "m=0,1,2,...; n=1,2,3,..."]
            ][series]
    }


def get_subscript(n: int):
    final = ''
    if n == 1:
        return ''
    for x in str(n):
        final += subscripts[int(x)]
    return final


def generate_name(name):
    carbon, series, location = parse_suffix_prefix(name)
    carbon += 1
    series += 1
    match series:
        case 1:
            return f'C{get_subscript(carbon + 1)}H{get_subscript((2 * (carbon + 1)) + 2)}'
        case 2:
            return f'C{get_subscript(carbon + 1)}H{get_subscript((2 * (carbon + 1)))}'
        case 3:
            return f'C{get_subscript(carbon + 1)}H{get_subscript((2 * (carbon + 1)) - 2)}'
        case 4:
            return f'C{get_subscript(carbon)}H{get_subscript((2 * (carbon)) + 1)}OH'
        case 5:
            return f'C{get_subscript(carbon - 1)}H{get_subscript((2 * (carbon - 1)) + 1)}COOH'
        case 6:
            return f'C{get_subscript(carbon - 1)}H{get_subscript((2 * (carbon - 1)) + 1)}COOCₙH₂ₙ₊₁'
        case _:
            pass
    

def image_from_list(list_input):
    field = Image.new("RGB", (segment_width * sum([image_library[i][1] for i in list_input]), segment_height), 'white')
    index = 0
    for x in list_input:
        field.paste(image_library[x][0], (index * segment_width, 0), image_library[x][0])
        index += image_library[x][1]
    return field

def image_generate(name):
    name = fix_input(name)
    carbon, series, location = parse_suffix_prefix(name)
    carbon += 1
    series += 1
    match series:
        case 1:
            field = ['' for i in range(carbon + 2)]
            field[0] = 'h-'
            field[-1] = '-h'
            for index, x in enumerate(field):
                if x:
                    continue
                field[index] = '-h-c-h-'
            image_from_list(field).save(f'chemistry_assets/library/{name}.png')
            return True
        case 2:
            field = ['' for i in range(carbon + 2)]
            field[location] = '-h-c=c-h-'
            field[0] = 'h-'
            field[-1] = '-h'
            for index, x in enumerate(field):
                if x:
                    continue
                field[index] = '-h-c-h-'
            image_from_list(field).save(f'chemistry_assets/library/{name}.png')
            return True
        case 3:
            field = ['' for i in range(carbon + 1)]
            field[location] = '-c==c-'
            field[0] = 'h-'
            field[-1] = '-h'
            for index, x in enumerate(field):
                if x:
                    continue
                field[index] = '-h-c-h-'
            image_from_list(field).save(f'chemistry_assets/library/{name}.png')
            return True
        case 4:
            field = ['' for i in range(carbon + 2)]
            field[location] = '-c-o-h'
            field[0] = 'h-'
            field[-1] = '-h'
            for index, x in enumerate(field):
                if x:
                    continue
                field[index] = '-h-c-h-'
            image_from_list(field).save(f'chemistry_assets/library/{name}.png')
            return True
        case 5:
            field = ['' for i in range(carbon + 2)]
            field[0] = 'h-'
            field[-2] = '-c=o-'
            field[-1] = '-o-h'
            for index, x in enumerate(field):
                if x:
                    continue
                field[index] = '-h-c-h-'
            image_from_list(field).save(f'chemistry_assets/library/{name}.png')
            return True
        case _:
            pass
    return False

initialize()
#print(generate_name("decanoic acid"))
#print(fix_input('dec-7-ane'))
#parse_suffix_prefix("prop-1-anol")
