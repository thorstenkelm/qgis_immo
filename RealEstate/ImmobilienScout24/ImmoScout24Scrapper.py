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

from RealEstate.Geocoding.Geocoder import Geocoder

from RealEstate.ImmobilienScout24.ImmoDataModel import ImmoDataModel


class ImmoScout24Scrapper:

    IS24_URL = 'https://www.immobilienscout24.de'

    def __init__(self, url):
        self.url = url
        print("Die AusgangsUrl lautet: "+self.url)
        self.city = self.get_city()
        print("Es werden "+ str(self.get_numberOfPages())+" Seiten durchsucht")

    def execute(self):
        """
        Execute method to start the functions for data scraping
        :return pandas dataframe:
        """
        path = self.get_script_path()

        return self.ImmoscoutScrape(memoryLocation=path + "\\")


    def URLSplitter(self):
        """
        :return list:
        """
        L = (self.url.split('/'))

        if len(L) == 8:
            a = L[5].split('-')
            residence = a[0]
            payment = a[1]
            state = L[6]
            city = L[7]
            # splits the URL and gathers information if it is a house or flat, if it is for rent or to buy
            # and in which state/city the property is
            Liste = [residence, payment, state, city]

        # len(L)==9
        else:
            a = L[5].split('-')
            residence = a[0]
            payment = a[1]
            state = L[6] + "/" + L[7]
            city = L[8]
            # splits the URL and gathers information if it is a house or flat, if it is for rent or to buy
            # and in which state/city the property is
            Liste = [residence, payment, state, city]
        return Liste

    def get_city(self):
        """
        :return string:
        """
        return self.URLSplitter()[-1]

    def get_subpageUrl(self, property_id):
        """
        uses the returned main part of the URl and adds the
        parts to create the URL for the single property
        :param property_id:
        :return string:
        """

        return self.IS24_URL + '/' + property_id

    def get_soup(self):
        """
        Use of the BeautifulSoup4 package to get the source code of the URL
        :return soup:
        """

        try:
            return bs.BeautifulSoup(self.open_stream(),
                                'lxml')
        except Exception as e:
            print(str(datetime.now()) + ": " + str(e))


    def open_stream(self):
        """
        :return bytes:
        """

        return urllib.request.urlopen(self.url).read()

    def get_numberOfPages(self):
        """
        Gets the number of all pages for the chosen city/place
        :return int:
        """
        entries = self.get_real_estate_entries(self.get_soup())
        return entries['paging']['numberOfPages']

    def get_nextPage(self):
        """
        Searches in the source code for the href to the next page
        :return string:
        """
        entries = self.get_real_estate_entries(self.get_soup())
        return entries['paging']['next']['@xlink.href']

    @staticmethod
    def get_keyValues(soup):
        """
        filters the important data out of the source code
        :param soup:
        :return dict:
        """
        paragraph = str(soup.find_all("script"))
        key_values = paragraph.split("keyValues = ")[1]
        key_values_json = json.loads(key_values.split("}")[0] + str("}"))

        return pd.DataFrame(data=key_values_json,
                            index=[str(datetime.now())])

    @staticmethod
    def get_description(data, soup):
        """
        gets the description of each property
        :param data:
        :param property_id:
        :param soup:
        :return list:
        """
        try:
            description = []
            #description is placed in the pre tag of the source code
            for i in soup.find_all("pre"):
                description.append(i.text)
            data["description"] = str(description)
            return description

        except Exception as e:
            print(str(datetime.now()) + ": " + str(e))

    @staticmethod
    def DF2CSV(path, df):  # TODO ist der ausgabe pfad nicht als eingabe sinnvoll __init__?
        """
        function to transform a Pandas dataframe into a CSV
        :param path:
        :param df:
        :return none:
        """
        print("Creating CSV")

        date = str(datetime.now())[:19].replace(":", "").replace(".", "")
        path = path + date + ".csv"

        df.to_csv(path,
                  sep=';',
                  decimal=',',
                  encoding='utf-8',
                  date_label='timestamp')

    def get_real_estate_entries(self, soup):
        """
        :param soup:
        :return dict:
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
                        #entries = flatten(entries)
                        return entries
        return None

    @staticmethod
    def str_to_json(string):
        """
        Transforms string to JSON
        :param string:
        :return dict:
        """
        string = string.strip()
        string_json = json.loads((string[17:-1]))
        return string_json["searchResponseModel"]["resultlist.resultlist"]

    def ImmoscoutScrape(self, memoryLocation: str):
        """
        function to run through all pages and get data from each property
        :param memoryLocation:
        :return pandas dataframe:
        """
        all_pages = self.get_numberOfPages()
        current_page = 1

        # geocoder for geocoding addresses
        g = Geocoder()

        # daten container fuer alle datensaetze
        all_data=pd.DataFrame()
        df = pd.DataFrame()
        data=pd.DataFrame()
        # stops at last page
        while (current_page <= all_pages):


            try:
                # gathers the information out of the soup object for each property entry
                entries_information = self.get_real_estate_entries(self.get_soup())
                #return entries_information['paging', 'next', '@xlink.href']

                # filters all given information for relevant data
                resultEntry = entries_information['resultlistEntries'][0]['resultlistEntry']

                for property_main_page in resultEntry:

                    property_id = property_main_page['@id']

                    property_main_page = flatten(d=property_main_page,
                                              reducer=self.underscore_reducer)

                    # elements of sub page
                    property_sub_page = self.get_subpage(property_id, df)
                    property_sub_page = flatten(d=property_sub_page,
                                              reducer=self.underscore_reducer)

                    # connect data from sub page with main page data
                    # achtung nestes dict -> flatten
                    data_property = {**property_main_page, **property_sub_page}


                    mod = ImmoDataModel(data_property)

                    # geocode address and set coordinates
                    coord = g.geocode(mod.get_address())
                    mod.set_coordinates(coordinates=coord)



                    #inserat = inserat.append(property_sub_page)
                    #print(property_id)
                    data = data.append(mod.get_data(),
                                       sort=True)

                # add everything filtered into the dataframe
                # daten alle zu einem Datensatz zusammenfuehren
                # df = df.append(data, sort=True)
                # convert dataframe to CSV and save it to the chosen location
                self.DF2CSV(memoryLocation, data)

                # set Url to the next page to check
                next_page = self.get_nextPage()

                self.url = self.IS24_URL + next_page


            except Exception as e:
                print(str(datetime.now()) + ": " + str(e))

            # increment page
            current_page = current_page + 1
            all_data=all_data.append(data)

        return all_data
    def get_subpage(self, property_id, df):
        """
        Method to extract KeyValues(relevant data) out of the script tags for each property
        :param property_id:
        :param df:
        :return DataFrame:
        """

        try:
            url_subpage = self.get_subpageUrl(property_id)  # english and underscore

            url_h = self.url

            self.url=url_subpage

            soup = self.get_soup() # http mit in die url builder methode packen
            # Key Value Pairs aus HTMl ziehen und in JSON speichern

            self.url = url_h
            data = self.get_keyValues(soup)
            self.get_description(data, soup)  # TODO objektbeschreibung, ausstattung und lage enthalten? ja ist enthalten
            df = df.append(data, sort=True)
            return df

        except Exception as e:
            print(str(datetime.now()) + ": " + str(e))

    @staticmethod
    def underscore_reducer(k1, k2):
        if k1 is None:
            return k2
        else:
            return k1 + "_" + k2

    @staticmethod
    def get_script_path():
        """
        Function to set storage location to the location of the script file
        :return file Directory as string:
        """
        return os.path.dirname(os.path.abspath(__file__))



if __name__ == "__main__":
    # single property
    test_url = 'https://www.immobilienscout24.de/Suche/S-2/P-1/Wohnung-Miete/Rheinland-Pfalz/Zweibruecken/Ixheim'

    # url studyarea
    url = 'https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Nordrhein-Westfalen/Essen'

    # Initialization of the class
    my_Scraper = ImmoScout24Scrapper(url=url)

    # Run main method
my_Scraper.execute()
