from pathlib import Path

import random
import requests
from bs4 import BeautifulSoup

http_proxy = "http://10.10.1.10:3128"
https_proxy = "https://10.10.1.11:1080"
ftp_proxy = "ftp://10.10.1.10:3128"


class Config:
    arm_upper_letter = 'ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ'
    arm_lower_letter = 'աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆև'

    url = "https://bararanonline.com/"
    endpoint = "letter/"
    query = "?page="

    PAYLOAD = {}
    HEADERS = {}

    proxy = {
        "http": http_proxy,
        "https": https_proxy,
        "ftp": ftp_proxy
    }

    def URL(self, letter, page_id):
        print(f'{self.url}{self.endpoint}{letter}{self.query}{page_id}')
        return f'{self.url}{self.endpoint}{letter}{self.query}{page_id}'

    headers_list = [
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        },
        # Firefox 77 Windows
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        },
        # Chrome 83 Mac
        {
            "Connection": "keep-alive",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.google.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
        },
        # Chrome 83 Windows
        {
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.google.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9"
        }
    ]


def next_page(num=1):
    while True:
        yield num
        num += 1


class GenerateWordList:

    def __init__(self, config):
        self.config = config

    def __iter__(self):

        for letter in self.config.arm_lower_letter:
            for page in self.get_page_for(letter):
                print(page)
                yield BararanOnlineScraping(page).get_words()
                exit(0)

    def get_page_for(self, letter):
        page = next_page()
        while True:
            # response = requests.request(
            #     "GET",
            #     self.config.URL(letter, next(page)),
            #     headers=random.choice(self.config.headers_list),
            #     data=self.config.PAYLOAD,
            #     proxies=self.config.proxy
            # )
            r = requests.Session()
            r.headers = random.choice(self.config.headers_list)
            response = r.get(self.config.URL(letter, next(page)))
            if response.status_code != 200:
                break
            yield response.text


class BararanOnlineScraping(BeautifulSoup):

    def get_words(self):
        for link in self.find_all('a', {"class": "word-href"}):
            yield link.text.strip()


def write_word_list(words_list, file_name):
    with open(Path(file_name), mode='w') as file:
        for words in words_list:
            print(words)
            file.writelines('\n'.join(words))


if __name__ == '__main__':
    # from dbus.mainloop.glib import DBusGMainLoop
    # from autovpn import AutoVPN
    # from gi.repository import GLib as gobject
    # DBusGMainLoop(set_as_default=True)
    # loop = gobject.MainLoop()
    # AutoVPN("New VPN")
    # loop.run()

    config = Config()
    word_list = GenerateWordList(config)

    write_word_list(word_list, 'dictionary_hy.txt')
