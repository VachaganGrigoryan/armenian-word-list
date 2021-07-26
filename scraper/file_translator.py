from googletrans import Translator
from pathlib import Path


def reader(file_name):
    with open(Path(file_name)) as file:
        for line in file:
            yield line


def trans_generate(file_name, word_list, src, dest, translator=Translator()):
    with open(Path(file_name), mode='w') as file:
        for word in word_list:
            result = translator.translate(word, dest=dest)
            print(result.text)
            file.write(f'{result.text}\n')


def run():
    input_file = 'dictionary_en.txt'
    src = 'en'
    dest = 'hy'

    f_name = input_file.split(".")
    f_name.insert(1, f'_{dest}')
    output_file = '.'.join(f_name)

    # trans_generate(output_file, reader(input_file), src, dest)


if __name__ == '__main__':
    run()

    from googletrans import Translator

    translator = Translator()
    result = translator.translate('Mikä on nimesi', src='fi', dest='fr')

    print(result.src)
    print(result.dest)
    print(result.text)