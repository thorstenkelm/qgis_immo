#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib.request
import bs4 as bs
import pandas as pd


IW_URL = 'https://www.immowelt.de'


class ImmoWeltScrapper:

    def __init__(self, url):
        self.__url = url
        self.number_of_pages = None
        self.number_of_hits = None

    def execute(self):

        # Starting page
        soup = self.create_soup(url=self.url)

        # get main attributes
        self.number_of_pages = self.get_pages(soup)
        data = self.extract_utag(soup)
        self.number_of_hits = data["search_results"]
        page_number = data["search_page"]
        page_url = self.url

        df = pd.DataFrame()

        while page_number <= self.number_of_pages:

            # open page
            print("### Open page: ", page_number)
            page_soup = self.create_soup(page_url)
            # data = self.extract_utag(soup)
            # TODO extract data from main page

            entries = self.get_entries(soup=page_soup)

            for entry in entries:

                print("Open entry: ", entry)
                expose_soup = self.create_soup(self.build_expose_url(expose_id=entry))
                # TODO extract data from entry
                data = self.extract_utag(expose_soup)
                address = self.get_address(expose_soup)

                df.append(data, sort=True)

            # get next page url
            page_number, page_url = self.get_next_page(soup=page_soup)

    @staticmethod
    def build_url(url):
        return IW_URL + url

    @staticmethod
    def build_expose_url(expose_id):
        return IW_URL + '/expose/' + expose_id

    @staticmethod
    def create_soup(url):
        # TODO HTTP CODE CHECK
        stream = urllib.request.urlopen(url)
        return bs.BeautifulSoup(stream.read(), 'lxml')

    @staticmethod
    def get_expose_tag(tag):
        return tag.has_attr('name') and tag.name == 'a'

    @staticmethod
    def extract_utag(soup):
        # get all script elements
        for paragraph in soup.find_all('script'):
            if r"utag_data" in str(paragraph):
                script = str(paragraph).split('\n')
                for line in list(script):
                    if line.strip().startswith('var utag_data'):
                        return json.loads(line.strip()[16:-1])

    def get_entries(self, soup):
        entries = []
        # get all entries
        for paragraph in soup.find_all(self.get_expose_tag):
            entries.append(paragraph.get('name'))

        return entries

    @staticmethod
    def get_pages(soup):
        paragraph = soup.find_all('div',
                                  attrs={'class': 'site-numbers',
                                         'id': 'pnlPaging'})

        return int(paragraph[0].text.strip().split('\n').pop())

    def get_next_page(self, soup):
        try:
            paragraph = soup.find_all('a',
                                      attrs={'class': 'icon-angle-right',
                                             'id': 'nlbPlus'},
                                      href=True)
            url = self.unescape(self.build_url(paragraph[0]['href']))
            page = int(url.split('cp=')[-1])
            return page, url
        except ConnectionError:
            # Increment max page
            return self.number_of_pages + 1, None

    @staticmethod
    def get_address(soup):
        paragraph = soup.find_all('script',
                                  attrs={'type': 'text/javascript'})

        for script in paragraph:
            if r"MapOptions" in str(script):
                for line in str(script).split('\n'):
                    if r"MapOptions" in line:
                        return json.loads(line.strip()[12:-1])

    @staticmethod
    def unescape(s):
        return s.replace("&amp;", "&")

    @property
    def url(self):
        return self.__url


i = ImmoWeltScrapper("https://www.immowelt.de/liste/essen/wohnungen/mieten?sort=relevanz")
i.execute()
