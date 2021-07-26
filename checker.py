from pathlib import Path
from utils import soundex, levenshtein


def read_file(file_name):
    with open(Path(file_name)) as file:
        for line in file:
            yield line.strip()


def soundex_words_mapping(words, text):
    maps = {}
    for word in words:
        s_code = soundex(word)
        if text == word:
            return {s_code: [word]}
        if s_code in maps:
            maps[s_code].append(word)
        else:
            maps[s_code] = [word]

    return maps


def spell_correction(text, dict_path='./dictionary/dictionary_hy.txt'):
    mapping = soundex_words_mapping(read_file(dict_path), text)
    text_soundex = soundex(text)
    possible_options = mapping.get(text_soundex)
    print(text_soundex, possible_options)

    if not possible_options:
        return []

    lev_dist = {}
    for word in possible_options:
        dist = levenshtein(text, word)
        if dist in lev_dist:
            lev_dist[dist].append(word)
        else:
            lev_dist[dist] = [word]

    return lev_dist.get(min(lev_dist.keys()))


if __name__ == '__main__':
    pass