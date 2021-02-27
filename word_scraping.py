from pathlib import Path

import requests
from bs4 import BeautifulSoup

from lxml.html import fromstring
from itertools import cycle

from const import proxies

import logging

logging.basicConfig(format="Datetime :: %(asctime)s %(message)s", level=logging.INFO)


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    logging.info(f'Proxies List: {proxies}')
    return proxies


class Config:
    arm_upper_letter = 'ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ'
    # arm_lower_letter = 'աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆև'
    arm_lower_letter = 'փքօֆև'

    url = "https://bararanonline.com/"
    endpoint = "letter/"
    query = "?page="

    PAYLOAD = {}
    HEADERS = {}

    # proxies = get_proxies()
    proxy_pool = cycle(proxies)

    def URL(self, letter, page_id):
        return f'{self.url}{self.endpoint}{letter}{self.query}{page_id}'


def next_page(num=1):
    while True:
        yield num
        num += 1


class GenerateWordList:

    def __init__(self, config):
        self.config = config
        self.proxy = next(self.config.proxy_pool)

    def __iter__(self):

        for letter in self.config.arm_lower_letter:
            logging.info(f'Getting the {letter} letter.')
            for page in self.get_page_for(letter):
                yield BararanOnlineScraping(page, features="lxml").get_words()
                # exit(0)

    def get_page_for(self, letter):

        page = next_page()  # 68 if letter == 'բ' else 1
        while True:
            status_code = False
            response_text = ''
            page_id = next(page)
            logging.info(f'Request: {self.config.URL(letter, page_id)}')
            while True:
                try:
                    # proxy = next(self.config.proxy_pool)
                    logging.info(f'Proxy IP: {self.proxy}')
                    response = requests.request(
                        "GET",
                        self.config.URL(letter, page_id),
                        headers=self.config.HEADERS,
                        data=self.config.PAYLOAD,
                        proxies={"http": self.proxy, "https": self.proxy}
                    )
                except:
                    logging.info(f"Connection error: Skipping... {self.proxy} IP.")
                    self.proxy = next(self.config.proxy_pool)
                else:
                    logging.info(f"Response Status Code: {response.status_code}")

                    if 'CAPTCHA' in response.text or 'captcha' in response.text:
                        logging.info(f"Captcha is activated: Skipping... {self.proxy} IP.")
                        self.proxy = next(self.config.proxy_pool)
                        continue

                    status_code = response.status_code != 200
                    response_text = response.text

                    Path(f'./html/{letter}').mkdir(parents=True, exist_ok=True)
                    with open(Path(f'./html/{letter}/{page_id}.html'), mode='w') as html:
                        html.write(response_text)
                    break
            if status_code:
                break

            yield response_text


class BararanOnlineScraping(BeautifulSoup):

    def get_words(self):
        return [link.text.strip() for link in self.find_all('a', {"class": "word-href"})]


def write_word_list(words_list, file_name, mode):
    with open(Path(file_name), mode=mode) as file:
        for words in words_list:
            lines = '\n'.join(words)
            logging.info(f'Here is the Words:\n{lines}')
            file.writelines(f'{lines}\n')


if __name__ == '__main__':
    config = Config()
    word_list = GenerateWordList(config)

    write_word_list(word_list, 'dictionary_hy.txt', 'a')
