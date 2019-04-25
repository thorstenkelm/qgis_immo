#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib.request
import bs4 as bs
import pandas as pd
import os, sys


IS24_URL = 'https://www.immobilienscout24.de'


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


class ImmoScout_MainPage:

    def __init__(self, url):
        self.__url = url

    def execute(self):

        # Starting page
        soup = self.create_soup(url=self.url)
        main_entries = self.get_real_estate_entries(soup=soup)

        # get main attributes
        number_of_pages = main_entries['paging']['numberOfPages']
        number_of_hits = main_entries['paging']['numberOfHits']
        search_description = main_entries['description']['text']
        page_url = next(iter(main_entries['paging']['current'].values()))
        page_number = main_entries['paging']['pageNumber']

        print('Search description: ', search_description)
        print('Number of properties: ', number_of_hits)
        print('Number of pages: ', number_of_pages)

        df = pd.DataFrame()

        # page iteration
        while page_number <= number_of_pages:

            print("Current Page: ", page_number)

            # open page
            soup = self.create_soup(self.build_url(url=page_url))
            main_entries = self.get_real_estate_entries(soup=soup)

            # get real estate entries
            entries = self.get_entries(main_entries=main_entries)

            # multiple objects on page as list
            if type(entries) == list:
                for entry in entries:
                    data = self.extract_data(entry)
                    # TODO Create data model and add information

                    expose_id = data['@id']
                    title = data['title']
                    address = data['address']
                    price = data['price']['value']
                    calculated_price = data['calculatedPrice']

            # single object on page as dict
            elif type(entries) == dict:
                data = self.extract_data(entries)
                print(data['address'])

            page_url = self.increment_url(main_entries)
            page_number = main_entries['paging']['pageNumber'] + 1

    @staticmethod
    def increment_url(main_entries):
        try:
            return next(iter(main_entries['paging']['next'].values()))
        except:
            return None

    @staticmethod
    def build_url(url):
        return IS24_URL + url

    @staticmethod
    def build_expose_url(expose_id):
        return IS24_URL + '/expose/' + expose_id

    @staticmethod
    def create_soup(url):
        # TODO HTTP CODE CHECK
        stream = urllib.request.urlopen(url)
        return bs.BeautifulSoup(stream.read(), 'lxml')

    # @staticmethod
    # def get_exposes(soup):
    #     exposes = []
    #     # get all a elements
    #     for paragraph in soup.find_all("a"):
    #         # get expose href elements
    #         if r"/expose/" in str(paragraph.get("href")):
    #             # collect expose links to list
    #             exposes.append(paragraph.get("href").split("#")[0])
    #         exposes = list(set(exposes))
    #     return exposes

    def get_real_estate_entries(self, soup):
        # get all script elements
        for paragraph in soup.find_all("script"):
            # get exposes script element
            if r"IS24.resultList" in str(paragraph):
                # split by line break
                script = list(str(paragraph).split('\n'))
                for line in list(script):
                    # get result model list
                    if line.strip().startswith('resultListModel'):
                        # convert str to json
                        entries = self.str_to_json(string=line)
                        return entries
        return None

    @staticmethod
    def str_to_json(string):
        string = string.strip()
        string_json = json.loads(string[17:-1])
        return string_json["searchResponseModel"]["resultlist.resultlist"]

    @staticmethod
    def get_entries(main_entries):
        return main_entries["resultlistEntries"][0]["resultlistEntry"]

    def extract_data(self, entry):
        entry = entry["resultlist.realEstate"]
        url = self.build_expose_url(entry['@id'])
        print(url)
        return entry

    @property
    def url(self):
        return self.__url


i = ImmoScout_MainPage(
    "https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Nordrhein-Westfalen/Bochum/Suedinnenstadt?enteredFrom=result_list")
i.execute()
i.url
