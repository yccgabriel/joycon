to_morse = {
    'a': '.-',
    'b': '-...',
    'c': '-.-.',
    'd': '-..',
    'e': '.',
    'f': '..-.',
    'g': '--.',
    'h': '....',
    'i': '..',
    'j': '.---',
    'k': '-.-',
    'l': '.-..',
    'm': '--',
    'n': '-.',
    'o': '---',
    'p': '.--.',
    'q': '--.-',
    'r': '.-.',
    's': '...',
    't': '-',
    'u': '..-',
    'v': '...-',
    'w': '.--',
    'x': '-..-',
    'y': '-.--',
    'z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
}
to_char = dict([reversed(i) for i in to_morse.items()]) # https://stackoverflow.com/a/3318808

to_charchar = {
    'a': {'r','zl'}, #'.-',
    'b': {'zr','l','a','left'}, #'-...',
    'c': {'zr','l','x','left'}, #'-.-.',
    'd': {'zr','l','a'}, #'-..',
    'e': {'r'}, #'.',
    'f': {'r','l','x','left'}, #'..-.',
    'g': {'zr','zl','a'}, #'--.',
    'h': {'r','l','a','left'}, #'....',
    'i': {'r','l'}, #'..',
    'j': {'r','zl','x','up'}, #'.---',
    'k': {'zr','l','x'}, #'-.-',
    'l': {'r','zl','a','left'}, #'.-..',
    'm': {'zr','zl'}, #'--',
    'n': {'zr','l'}, #'-.',
    'o': {'zr','zl','x'}, #'---',
    'p': {'r','zl','x','left'}, #'.--.',
    'q': {'zr','zl','a','up'}, #'--.-',
    'r': {'r','zl','a'}, #'.-.',
    's': {'r','l','a'}, #'...',
    't': {'zr'}, #'-',
    'u': {'r','l','x'}, #'..-',
    'v': {'r','l','a','up'}, #'...-',
    'w': {'r','zl','x'}, #'.--',
    'x': {'zr','l','a','up'}, #'-..-',
    'y': {'zr','l','x','up'}, #'-.--',
    'z': {'zr','zl','a','left'}, #'--..',
}

def decode(combo):
    if combo == {'r','zl'}:
        return 'a'
    elif combo == {'zr','l','a','left'}:
        return 'b'
    elif combo == {'zr','l','x','left'}:
        return 'c'
    elif combo == {'zr','l','a'}:
        return 'd'
    elif combo == {'r'}:
        return 'e'
    elif combo == {'r','l','x','left'}:
        return 'f'
    elif combo == {'zr','zl','a'}:
        return 'g'
    elif combo == {'r','l','a','left'}:
        return 'h'
    elif combo == {'r','l'}:
        return 'i'
    elif combo == {'r','zl','x','up'}:
        return 'j'
    elif combo == {'zr','l','x'}:
        return 'k'
    elif combo == {'r','zl','a','left'}:
        return 'l'
    elif combo == {'zr','zl'}:
        return 'm'
    elif combo == {'zr','l'}:
        return 'n'
    elif combo == {'zr','zl','x'}:
        return 'o'
    elif combo == {'r','zl','x','left'}:
        return 'p'
    elif combo == {'zr','zl','a','up'}:
        return 'q'
    elif combo == {'r','zl','a'}:
        return 'r'
    elif combo == {'r','l','a'}:
        return 's'
    elif combo == {'zr'}:
        return 't'
    elif combo == {'r','l','x'}:
        return 'u'
    elif combo == {'r','l','a','up'}:
        return 'v'
    elif combo == {'r','zl','x'}:
        return 'w'
    elif combo == {'zr','l','a','up'}:
        return 'x'
    elif combo == {'zr','l','x','up'}:
        return 'y'
    elif combo == {'zr','zl','a','left'}:
        return 'x'
    else:
        return '\a'
    # print('combo:', combo)
    # if combo == {'r'}:
    #     s = '.'
    # elif combo == {'zr'}:
    #     s = '-'
    # elif combo == {'r', 'l'}:
    #     s = '..'
    # elif combo == {'r', 'zl'}:
    #     s = '.-'
    # else:
    #     return 'unknown'

    try:
        return to_char[combo]
    except KeyError:
        return '\a'
