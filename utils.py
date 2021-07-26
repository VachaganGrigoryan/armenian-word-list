def levenshtein(a, b):

    lev = [
        [
            i + j if i == 0 or j == 0 else None for j in range(len(b) + 1)
        ] for i in range(len(a) + 1)
    ]

    for i in range(1, len(lev)):
        for j in range(1, len(lev[i])):
            if a[i - 1] == b[j - 1]:
                lev[i][j] = lev[i - 1][j - 1]
            else:
                lev[i][j] = min(lev[i - 1][j], lev[i][j - 1], lev[i - 1][j - 1]) + 1

    return lev[-1][-1]


def soundex(text):
    text = text.lower()
    # encoding_table = {
    #     '': 'AEHIOUWY',
    #     '1': 'BFPV',
    #     '2': 'CGJKQSXZ',
    #     '3': 'DT',
    #     '4': 'L',
    #     '5': 'MN',
    #     '6': 'R'
    # }
    encoding_table = {
        '':  'աեէիյհօուըև',
        '1': 'բֆփվպ',
        '2': 'սցգԺծքկխզթձճղշչջ',
        '3': 'դտ',
        '4': 'լ',
        '5': 'մն',
        '6': 'ռր',
    }
    					
    soundex_number = text[0]
    for symboly in text[1:]:
        for number in encoding_table:
            if symboly in encoding_table[number]:

                soundex_number = f'{soundex_number}{number}'

    return f'{soundex_number[:4]:0<4s}'


if __name__ == '__main__':

    print(soundex("Կավո"))
    print(soundex("կոքոս"))
    print(soundex('կիղի'))
    print(soundex('արավ'))
    print(soundex('ծանռ'))
    print(soundex('նորուդյուն'))
    print(soundex('հայկո'))