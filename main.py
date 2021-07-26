from utils import levenshtein, soundex
from checker import spell_correction


def run(option):
    def option_levenshtein():
        a, b = input("First string: "), input("Second string: ")
        return f'Levenshtein distance for "{a}" and "{b}" is {levenshtein(a, b)}'

    def option_soundex():
        word = input("Input string: ")
        return f'Soundex code for "{word}" is {soundex(word)}'

    def option_spell_correction():
        word = input('Write misspelled word: ')
        return f'Possible options: {", ".join(spell_correction(word, "./dictionary/dictionary_hy.txt"))}'

    _func = {
        '1': option_levenshtein,
        '2': option_soundex,
        '3': option_spell_correction
    }
    method = _func.get(option, lambda: ValueError("The options is not valid. Please Type 1, 2 or 3."))
    print(method())


option = input(
    'Choose from options: '
    '\n1. Levenshtein'   
    '\n2. Soundex'
    '\n3. Spell correction'
    '\nType 1, 2 or 3: '
)
run(option)