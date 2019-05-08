import pandas as pd
import os
import bs4 as bs
import urllib.request
from datetime import datetime
import json



'''Class to scrape relevant data from an Immoscout24-URL'''
class Scraper:
    #Parameters:
    #Class has to be initialised with the url of the first page of chosen city

    def __init__(self, url):
        self.url = url


    def execute(self):
        '''Execute method to start the functions for data scraping'''
        #data will be saved into csv format and saved to the location of the script
        path = get_script_path()
        self.ImmoscoutScrape(path + "\\")


    def URLSplitter(self):
        '''splits the URL and returns the main page, so the
        varying parts of the URL can later be added'''
        L = (self.url.split('/'))
        return L[2]

    def get_URLUnterseite(self, exposeid):
        '''uses the returned main part of the URl and adds the
        parts to create the URL for the single exposé'''
        return self.URLSplitter() + '/' + exposeid

    def get_soup(self):
        '''Use of the BeautifulSoup4 package to get the source code of the URL'''
        return bs.BeautifulSoup(urllib.request.urlopen(self.url).read(), 'lxml')

    def get_numberOfPages(self):
        '''Gets the number of all pages for the chosen city/place'''
        entries = self.get_real_estate_entries(self.get_soup())
        return entries['paging']['numberOfPages']

    def get_nextPage(self):
        '''Searches in the source code for the href to the next page'''
        entries = self.get_real_estate_entries(self.get_soup())
        return entries['paging']['next']['@xlink.href']

    def get_keyValues(self, soup):
        '''filters the important data out of the source code'''
        data = pd.DataFrame(
            json.loads(str(soup.find_all("script")).split("keyValues = ")[1].split("}")[0] + str("}")),
            index=[str(datetime.now())])
        return data

    def get_description(self, data, exposeid, soup):
        '''gets the description of each exposé'''
        data["URL"] = str(exposeid)
        description = []
        #description is placedd in the pre tag of the source code
        for i in soup.find_all("pre"):
            description.append(i.text)
        data["description"] = str(description)





    def DF2CSV(self, Pfad, df):  # Pandas dataframe
        '''function to transform a Pandas dataframe into a CSV'''
        print("Exportiert CSV")

        df.to_csv(
            Pfad + str(datetime.now())[:19].replace(":", "").replace(
            ".", "") + ".csv", sep=";",
            decimal=",", encoding="utf-8", index_label="timestamp")  # Utf-8 anpassen

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
                        #entries = flatten(entries)
                        return entries
        return None


    @staticmethod
    def str_to_json(string):
        '''Transforms string to JSON'''
        string = string.strip()
        string_json = json.loads((string[17:-1]))
        return string_json["searchResponseModel"]["resultlist.resultlist"]



    def ImmoscoutScrape(self, memoryLocation: str):
        '''function to run through all pages and get data from each exposé'''
        allPages = self.get_numberOfPages()
        currentPage=1
        #stops at last page
        while (currentPage <= allPages):
            df = pd.DataFrame()
            data = pd.DataFrame()
            try:
                entries = self.get_real_estate_entries(self.get_soup())
                #return entries['paging', 'next', '@xlink.href']
                resultEntry = entries['resultlistEntries'][0]['resultlistEntry']
                for i in resultEntry:
                    inserat = pd.DataFrame(i, index=[i['@id']])
                    exposeid = i['@id']
                    inserat = inserat.append(self.get_Unterseite(exposeid, df))
                    #print(exposeid)
                    data = data.append(inserat, sort=True)



                """
                hier johannes marlena teil
                """


                #add everything filtered into the dataframe
                df = df.append(data, sort=True)
                #convert dataframe to CSV and save it to the chosen location
                self.DF2CSV(memoryLocation, df)

               #set Url to the next page to check
                nextPage=self.get_nextPage()
                self.url = "https://www.immobilienscout24.de" + nextPage
                print(self.url)

            except Exception as e:
                print(str(datetime.now()) + ": " + str(e))

            currentPage = currentPage + 1

    def get_Unterseite(self, exposeid, df):
        urlUnterseite = self.get_URLUnterseite(exposeid)

        '''Method to extract KeyValues(relevant data) out of the script tags for each exposé'''
        try:
            soup = bs.BeautifulSoup(urllib.request.urlopen('http://' + urlUnterseite).read(),'lxml')
            # Key Value Pairs aus HTMl ziehen und in JSON speichern
            data = self.get_keyValues(soup)
            self.get_description(data, exposeid, soup)
            df = df.append(data, sort=True)
        except Exception as e:
            print(str(datetime.now()) + ": " + str(e))

        return df




def get_script_path():
    '''Function to set storage location to the location of the script file'''
    return os.path.dirname(os.path.abspath(__file__))

#Initialisierung der Klasse
#my_Scraper = Scraper("https://www.immobilienscout24.de/Suche/S-2/P-1/Wohnung-Miete/Rheinland-Pfalz/Zweibruecken/Ixheim", get_script_path())
my_Scraper = Scraper("https://www.immobilienscout24.de/Suche/S-2/P-1/Haus-Kauf/Nordrhein-Westfalen/Essen")
#Ausführen der Main-Methode
my_Scraper.execute()



