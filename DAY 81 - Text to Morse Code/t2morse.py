## Text to Morse Code import file

valid = '-·.'

# text to morse code equivalents
codes = {
    'A': '· -', 'B': '- · · ·', 'C': '- · - ·',
    'D': '- · ·', 'E': '·', 'F': '· · - ·',
    'G': '- - ·', 'H': '· · · ·', 'I': '· ·',
    'J': '· - - -', 'K': '- · -', 'L': '· - · ·',
    'M': '- -', 'N': '- ·', 'O': '- - -',
    'P': '· - - ·', 'Q': '- - · -', 'R': '· - ·',
    'S': '· · ·', 'T': '-', 'U': '· · -',
    'V': '· · · -', 'W': '· - -', 'X': '- · · -',
    'Y': '- · - -', 'Z': '- - · ·',

    '1': '· - - - -', '2': '· · - - -', '3': '· · · - -',
    '4': '· · · · -', '5': '· · · · ·', '6': '- · · · ·',
    '7': '- - · · ·', '8': '- - - · ·', '9': '- - - - ·',
    '0': '- - - - -'
}

# morse code to text equivalents
characters = {
    '· -': 'A', '- · · ·': 'B', '- · - ·': 'C',
    '- · ·': 'D', '·': 'E', '· · - ·': 'F',
    '- - ·': 'G', '· · · ·': 'H', '· ·': 'I',
    '· - - -': 'J', '- · -': 'K', '· - · ·': 'L',
    '- -': 'M', '- ·': 'N', '- - -': 'O',
    '· - - ·': 'P', '- - · -': 'Q', '· - ·': 'R',
    '· · ·': 'S', '-': 'T', '· · -': 'U',
    '· · · -': 'V', '· - -': 'W', '- · · -': 'X',
    '- · - -': 'Y', '- - · ·': 'Z',

    '· - - - -': '1', '· · - - -': '2', '· · · - -': '3',
    '· · · · -': '4', '· · · · ·': '5', '- · · · ·': '6',
    '- - · · ·': '7', '- - - · ·': '8', '- - - - ·': '9',
    '- - - - -': '0'
}


def convert_to_morse(text):
    """Takes in string as an argument to convert into morse code. This function
       follows the international convention, with spaces between parts of the 
       same letter, three spaces between each letter, and seven spaces between words."""
    out = ''
    for c in text.upper():
        if c == ' ':
            out += '       '
        elif c in codes:
            out += codes[c] + '   '

    return out


def convert_to_text(code):
    """Takes in morse code as an argument to convert into text. This function
       follows the international convention, which means the text to be passed
       must be in the right format. More information on https://en.wikipedia.org/wiki/Morse_code"""

    out = ''
    spaces = 0

    # variable to hold dots and dashes
    char_code = ''
    for c in code + '\n':
        
        # if spaces counted is already 7
        if spaces == 7:
            out += ' '
            spaces = 0
        elif c == ' ':
            spaces += 1
        elif c in valid:
            if c == '.':
                char_code += '·'
            else:
                char_code += c
            spaces = 0

        if spaces == 3 or c == '\n':

            # a special case in which if I use this program in the future, and just copy paste a code, which means it doesn't
            # naturally have a terminating character put in place.
            if char_code == '' and c == '\n':
                break
            
            out += characters[' '.join(char_code)]
            char_code = ''


    return out.lower()