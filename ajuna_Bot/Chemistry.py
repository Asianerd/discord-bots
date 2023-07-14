def hydrocarbon(name: str):
    # functional group
    # general formula
    # structural formula
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
    prefixes = ['meth', 'eth', 'prop', 'but', 'pent', 'hex', 'hept', 'oct', 'non', 'dec']
    suffixes = ['ane', 'ene', 'yne', 'ol', 'oic', 'oate']
    carbon = [index for index, i in enumerate(prefixes) if name.startswith(i)][0] if [index + 1 for index, i in enumerate(prefixes) if name.startswith(i)] else -1
    series = [index for index, i in enumerate(suffixes) if name.endswith(i)][0] if [index + 1 for index, i in enumerate(suffixes) if name.endswith(i)] else -1
    if (carbon + series) == -2:
        return False
    return {
        # ⁰¹²³⁴⁵⁶⁷⁸⁹
        # ₀₁₂₃₄₅₆₇₈₉
        # ⁺⁻⁼⁽⁾ⁿ ₊₋ ₘₙ
        'carbon': carbon + 1,
        'h_series': 'alkane,alkene,alkyne,alcohol,carboxylic acid,ester'.split(',')[series].capitalize(),
        'f_group': 'Single bond between carbon atoms,Double bond between carbon atoms,Triple bond between carbon atom,Hydroxl,Carboxyl,Carboxylate'.split(',')[series],
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
