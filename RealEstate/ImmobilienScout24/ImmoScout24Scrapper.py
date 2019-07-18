"""
Description: # TODO class description is missing
Author:

Class to scrape relevant data from an Immoscout24-URL
Class has to be initialised with the url of the first page of chosen city
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
        # TODO parameters like city, number of pages for example save in object

    def execute(self):
        """
        Execute method to start the functions for data scraping
        :return:
        """
        path = self.get_script_path()
        self.ImmoscoutScrape(memoryLocation=path + "\\")
        # TODO missing return

    def URLSplitter(self):  # TODO rename method url_splitter
        """
        splits the URL and returns the main page, so the
        varying parts of the URL can later be added
        :return:
        """
        return self.url.split('/')[2]  # TODO if possible direct return - like this

    def get_URLUnterseite(self, expose_id):  # TODO rename class to english with underscore, build_url?
        """
        uses the returned main part of the URl and adds the
        parts to create the URL for the single exposé
        :param expose_id:
        :return:
        """
        return self.URLSplitter() + '/' + expose_id  # TODO rename parameter with underscore like this

    def get_soup(self):  # TODO Execption handling?
        """
        Use of the BeautifulSoup4 package to get the source code of the URL
        :return:
        """
        return bs.BeautifulSoup(self.open_stream(),  # TODO zur uebersichtlichkeit jeder parameter in eine eigene Zeile, wenn möglich mit parametername = parameter
                                'lxml')

    def open_stream(self):
        """

        :return:
        """
        stream = urllib.request.urlopen(self.url).read()  # TODO jede Klasse soll eine Aufgabe haben
        return stream

    def get_numberOfPages(self):  # TODO rename method with underscore
        """
        Gets the number of all pages for the chosen city/place
        :return:
        """
        entries = self.get_real_estate_entries(self.get_soup())
        return entries['paging']['numberOfPages']

    def get_nextPage(self):  # TODO s.o.
        """
        Searches in the source code for the href to the next page
        :return:
        """
        entries = self.get_real_estate_entries(self.get_soup())
        return entries['paging']['next']['@xlink.href']

    def get_keyValues(self, soup):  # TODO s.o. und wenn self nicht gebraucht wird, kennzeichnet die methode als static  -> @staticmethod
        """
        filters the important data out of the source code
        :param soup:
        :return:
        """
        paragraph = str(soup.find_all("script"))  # TODO gewoehnt euch an, komplexe konstruktre zu vereinfachen
        key_values = paragraph.split("keyValues = ")[1]
        key_values_json = json.loads(key_values.split("}")[0] + str("}"))

        return pd.DataFrame(data=key_values_json,
                            index=[str(datetime.now())])

    def get_description(self, data, exposeid, soup):  # TODO falls keine Beschreibung gefunden wurde try except
        """
        gets the description of each exposé
        :param data:
        :param exposeid:
        :param soup:
        :return:
        """
        data["URL"] = str(exposeid)  # Wieso wird hier die zuweisung durchgefuehrt?
        description = []
        #description is placedd in the pre tag of the source code
        for i in soup.find_all("pre"):
            description.append(i.text)  # ist jedes pre = beschreibung? gff. weiter filtern?
        data["description"] = str(description)  # methoden lieber mit return und keine direkte zuweisung, macht die in der eigenlichen logik damit bleibt der code konsistent und einheitlich / nachvollziehbar

    def DF2CSV(self, Pfad, df):  # TODO variablen umbenennen - englisch, ist der ausgabe pfad nicht als eingabe sinnvoll __init__?
        """
        function to transform a Pandas dataframe into a CSV
        :param Pfad:
        :param df:
        :return:
        """
        print("Exportiert CSV")  # english

        date = str(datetime.now())[:19].replace(":", "").replace(".", "")
        path = Pfad + date + ".csv"

        df.to_csv(path,
                  sep=';',
                  decimal=',',
                  encoding='utf-8',
                  index_label='timestamp')  # TODO index umbenennen timestamp suggeriert das einstelldatum

    def get_real_estate_entries(self, soup):
        """

        :param soup:
        :return:
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
        :return:
        """
        string = string.strip()
        string_json = json.loads((string[17:-1]))
        return string_json["searchResponseModel"]["resultlist.resultlist"]

    def ImmoscoutScrape(self, memoryLocation: str):
        """
        function to run through all pages and get data from each exposé
        :param memoryLocation:
        :return:
        """
        allPages = self.get_numberOfPages()  # TODO variable lower case
        currentPage = 1  # TODO variable underscore

        # geocoder for geocoding addresses
        g = Geocoder()

        # daten container fuer alle datensaetze
        data = pd.DataFrame()

        # stops at last page
        while (currentPage <= allPages):
            #df = pd.DataFrame()

            try:
                # was passiert hier? immer beschreiben
                entries = self.get_real_estate_entries(self.get_soup())  # Das wuerde ich in Beschreibung umbenennen
                #return entries['paging', 'next', '@xlink.href']

                # s.o.
                resultEntry = entries['resultlistEntries'][0]['resultlistEntry']  # als methode definieren - get_entries, mehrzahl

                for i in resultEntry:  # i = entry
                    # inserat = pd.DataFrame(i, index=[i['@id']])
                    exposeid = i['@id']

                    # elemente der hauptseite = i
                    # zusammenfassen mit underscore
                    expose_sub_page = flatten(d=i, # TODO variable umbenennen
                                              reducer=self.underscore_reducer)

                    # elemente der unterseite = inserat # TODO umbenennen
                    expose_sub_page = self.get_Unterseite(exposeid, df)

                    # zusammenfassen mit underscore
                    expose_sub_page = flatten(d=expose_sub_page,
                                              reducer=self.underscore_reducer)

                    # daten aus hauptseite mit unterseite zusammenfügen
                    # achtung nestes dict -> flatten
                    data_expose = {**i, **expose_sub_page}

                    """
                    hier johannes marlena teil
                    """

                    mod = ImmoDataModel(data_expose)

                    # geocode address and set coordinates
                    coord = g.geocode(mod.get_address())
                    mod.set_coordinates(coordinates=coord)



                    #inserat = inserat.append(expose_sub_page)
                    #print(exposeid)
                    data = data.append(mod.get_data(),
                                       sort=True)

                # add everything filtered into the dataframe
                # daten alle zu einem Datensatz zusammenfuehren
                # df = df.append(data, sort=True)
                # convert dataframe to CSV and save it to the chosen location
                self.DF2CSV(memoryLocation, data)

                # set Url to the next page to check
                nextPage = self.get_nextPage() # TODO rename variable
                self.url = self.IS24_URL + nextPage  # TODO Konstanten definieren
                print(self.url)  # fuer ausgaben immer mehr kontext :-)

            except Exception as e:
                print(str(datetime.now()) + ": " + str(e))

            # increment page
            currentPage = currentPage + 1

    def get_Unterseite(self, exposeid, df):  # TODO umbenennen
        """
        Method to extract KeyValues(relevant data) out of the script tags for each exposé
        :param exposeid: # TODO underscore
        :param df:
        :return:
        """


        try:
            urlUnterseite = self.get_URLUnterseite(exposeid)  # english and underscore

            soup = self.get_soup('http://' + urlUnterseite) # http mit in die url builder methode packen
            # Key Value Pairs aus HTMl ziehen und in JSON speichern
            data = self.get_keyValues(soup)
            self.get_description(data, exposeid, soup)  # TODO objektbeschreibung, ausstattung und lage enthalten?
            # get_description mit return
            # data = dataframe? -> data.append(description)
            df = df.append(data, sort=True)
        except Exception as e:
            print(str(datetime.now()) + ": " + str(e))

        return df # return in try - data als return

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
        :return:
        """
        return os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    # single expose
    test_url = 'https://www.immobilienscout24.de/Suche/S-2/P-1/Wohnung-Miete/Rheinland-Pfalz/Zweibruecken/Ixheim'

    # url studyarea
    url = 'https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Nordrhein-Westfalen/Essen' # TODO wir untersuchen mieten, keine haeuser :-)

    # Initialization of the class
    my_Scraper = ImmoScout24Scrapper(url=url)

    # Run main method
    my_Scraper.execute()
