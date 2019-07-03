"""
Description: Class to scrape relevant data from an Immoscout24-URL
Class has to be initialised with the url of the first page of chosen city
Author: Maximilian Haverkamp & Veronika Schmidt
"""

import pandas as pd
import os
import bs4 as bs
import urllib.request
from datetime import datetime
import json
from flatten_dict import flatten


from ImmoScrapper.Geocoder import Geocoder
from ImmoScrapper.ImmoDataModel import ImmoDataModel
from ImmoScrapper.BuildingReferences import BuildingReferences


class ImmoScout24Scrapper:

    IS24_URL = 'https://www.immobilienscout24.de'
    ACTIVE_ADVERTISEMENTS = "active_advertisements.csv"

    def __init__(self, url):
        self.url = url
        self.city = self.get_city()
        self.number_of_pages = self.get_number_of_pages()
        self.path = self.get_script_path()
        self.gebref = BuildingReferences(city=self.city,
                                         path=self.path)

        print("Starting URL: " + self.url)
        print("Number of pages: " + str(self.number_of_pages))

    def execute(self):
        """
        Execute method to start the functions for data scraping
        :return: Pandas DataFrame
        """
        return self.scrape()

    def url_splitter(self):
        """
        Splits the URL and gathers information if it is a house or flat, if it is for rent or to buy
        and in which state/city the property is
        :return list:
        """
        url_split = (self.url.split('/'))

        if len(url_split) == 8:
            element = url_split[5].split('-')
            residence = element[0]
            payment = element[1]
            state = url_split[6]
            city = url_split[7]

        else:
            element = url_split[5].split('-')
            residence = element[0]
            payment = element[1]
            state = url_split[6] + "/" + url_split[7]
            city = url_split[8]

        return {'residence': residence,
                'payment': payment,
                'state': state,
                'city': city}

    def get_city(self):
        """
        Get city from url
        :return: string
        """
        para = self.url_splitter()
        return para['city']

    def build_url(self, expose_id):
        """
        Uses the returned main part of the URl and adds the
        parts to create the URL for the single property
        :return: string
        """
        return self.IS24_URL + '/' + expose_id

    def get_soup(self):
        """
        Use of the BeautifulSoup4 package to get the source code of the URL
        :return soup:
        """
        try:
            return bs.BeautifulSoup(self.open_stream(),
                                    'lxml')
        except Exception as e:
            print("Get soup: ", str(datetime.now()) + ": " + str(e))

    def open_stream(self):
        """
        Open stream for bs4
        :return: Request-Object
        """
        return urllib.request.urlopen(self.url).read()

    def get_number_of_pages(self):
        """
        Gets the number of all pages for the chosen city/place
        :return: int
        """
        entries = self.get_real_estate_entries(self.get_soup())
        return entries['paging']['numberOfPages']

    def get_next_page(self):
        """
        Searches in the source code for the href to the next page
        :return string:
        """
        try:
            entries = self.get_real_estate_entries(self.get_soup())
            return entries['paging']['next']['@xlink.href']
        except KeyError as e:
            print(e)
            return ""

    @staticmethod
    def get_key_values(soup):
        """
        Filters the important data out of the source code
        :param: Soup
        :return: Dict
        """
        paragraph = str(soup.find_all("script"))
        key_values = paragraph.split("keyValues = ")[1]
        key_values_json = json.loads(key_values.split("}")[0] + str("}"))

        return key_values_json

    @staticmethod
    def get_description(soup):
        """
        gets the description of each property
        :param: bs4
        :param: Soup
        :return: List
        """
        try:
            # description is placed in the pre tag of the source code
            description = []

            for i in soup.find_all("pre"):
                description.append(i.text)

            return description

        except Exception as e:
            print("Get description: ", str(datetime.now()) + ": " + str(e))

    def build_result_path(self):
        date = str(datetime.now())[:19].replace(":", "").replace(".", "")
        return self.path + '-' + str(self.city) + '-' + date + '.csv'

    def df2csv(self, df):
        """
        Function to transform a Pandas DataFrame into a CSV
        """
        df.to_csv(self.build_result_path(),
                  sep=';',
                  decimal='.',
                  encoding='utf-8',
                  index=False)

    def get_real_estate_entries(self, soup):
        """
        Get entries from bs4
        """
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
        """
        Transforms string to JSON
        """
        string = string.strip()
        string_json = json.loads((string[17:-1]))
        return string_json["searchResponseModel"]["resultlist.resultlist"]

    def scrape(self):
        """
        function to run through all pages and get data from each property
        """
        try:
            current_page = 1

            # geocoder for geocoding addresses
            g = Geocoder(self.gebref)

            # data container
            df = pd.DataFrame()

            # stops at last page
            while current_page <= self.number_of_pages:
                print('Page: ', current_page)

                # gathers the information out of the soup object for each property entry
                entries_information = self.get_real_estate_entries(self.get_soup())

                # filters all given information for relevant data
                result_entry = entries_information['resultlistEntries'][0]['resultlistEntry']

                # iteration of exposes
                for property_main_page in result_entry:

                    property_id = property_main_page['@id']
                    print("Expose: ", property_id)

                    property_main_page = flatten(d=property_main_page,
                                                 reducer=self.underscore_reducer)

                    # elements of sub page
                    property_sub_page = self.get_sub_page(property_id)
                    property_sub_page = flatten(d=property_sub_page,
                                                reducer=self.underscore_reducer)

                    # add extraction time
                    property_sub_page['extraction_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # merge data
                    data_property = {**property_main_page, **property_sub_page}

                    mod = ImmoDataModel(data_property)

                    precise_house_number = mod.get_value('precise_house_number')
                    mod_coord = mod.check_coordinates()

                    if precise_house_number:

                        # get address
                        address = mod.get_address()

                        # geocode address and set coordinates
                        coord = g.get_coordinates(street=address['street'],
                                                  street_house_number=address['street_house_number'],
                                                  house_number_supplement=address['house_number_supplement'],
                                                  city=address['city'],
                                                  coord_available=mod_coord)

                        # no geocoding worked, set origin coordinates
                        if coord:
                            mod.set_coordinates(coordinates=coord)

                    # add data to result
                    df = df.append(mod.get_data)

                # set Url to the next page to check
                next_page = self.get_next_page()
                self.url = self.IS24_URL + next_page

                # increment page
                current_page = current_page + 1

            return df

        except Exception as e:
            print('Scrapper: ', str(datetime.now()) + ": " + str(e))
            return df

    def get_sub_page(self, property_id):
        """
        Method to extract KeyValues(relevant data) out of the script tags for each property
        """
        try:
            # build and store url
            url_sub_page = self.build_url(property_id)  # english and underscore
            url_h = self.url

            self.url = url_sub_page
            soup = self.get_soup()

            # restore url
            self.url = url_h

            # extract data
            data = self.get_key_values(soup)

            # data['description'] = self.get_description(data)

            return data

        except Exception as e:
            print(str(datetime.now()) + ": " + str(e))

    @staticmethod
    def underscore_reducer(k1, k2):
        """
        Method to flatten dict by underscore
        """
        if k1 is None:
            return k2
        else:
            return k1 + "_" + k2

    @staticmethod
    def get_script_path():
        """
        Function to set storage location to the location of the script file
        :return: file Directory as string
        """
        return os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    # url studyarea
    url = 'https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Nordrhein-Westfalen/Essen'

    # Initialization of the class
    my_Scraper = ImmoScout24Scrapper(url=url)

    # Run main method
    data = my_Scraper.execute()

    file_name = "-".join([datetime.now().strftime("%Y-%m-%d_%H_%M_%S"), my_Scraper.city]) + ".csv"

    data.to_csv(file_name,
                sep=';',
                decimal='.',
                encoding='utf-8',
                index=False)
