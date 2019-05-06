# -*- coding: utf-8 -*-
# Author: Thorsten Kelm, thorsten.kelm@hs-bochum.de

import urllib.request
import zipfile
from dfply import *



class BuildingReferences:

    #Konstruktor, der die Funktionen read_data, read_keys und get_city_key aufruft
    def __init__(self, gebref_path, gebref_keys_path, studyarea):
     #   self.download_data()
        self.__studyarea = studyarea
        self.__gebref_keys = self.read_keys(gebref_keys_path)
        self.__city_key = self.get_city_key()
        self.__gebref = self.read_data(gebref_path)


    #def download_data (self):
    #    print("Beginning file download...")
    #    url = 'https://www.opengeodata.nrw.de/produkte/geobasis/lika/alkis_sek/gebref/gebref_EPSG4647_ASCII.zip'
    #    save = 'C:/Users/Fabian Hannich/Desktop/gebref.zip'
    #    urllib.request.urlretrieve(url, save)
    #    print("..download ends!")

    #    print("Unpack data...")
    #    extractTo = "C:/Users/Fabian Hannich/Documents/Studium/6. Semester/GI-Projekt_Immo/Hauskoordinaten_gebref_EPSG4647_ASCII/"
    #    zipfile.ZipFile(save, 'r').extractall(extractTo)
    #    print("Data ready!")


    #read gebref-data and assign type
    def read_data(self, gebref_path):
        print("Read, filter and encoding gebref_data..")
        gebref_data = pd.read_csv(gebref_path,
                                  sep=';',
                                  decimal=',',
                                  header=None,
                                  names=['nba', 'oi', 'qua', 'lan', 'rbz', 'krs', 'gmd',
                                         'ott', 'sss', 'hsr', 'adz', 'east', 'north', 'stn'],
                                  usecols=['lan', 'rbz', 'krs', 'gmd', 'hsr',
                                           'adz', 'east', 'north', 'stn'],
                                  dtype={'lan': str, 'rbz': str, 'krs': str, 'gmd': str, 'hsr': str,
                                         'adz': str, 'east': float, 'north': float, 'stn': str},
                                  encoding='ISO-8859-1')

        #fill empty lines
        gebref_data.fillna('', inplace=True)

        #filter the gebref_data
        gebref_data = gebref_data >> mask(X.lan == self.__city_key['lan'].values[0],
                                                      X.rbz == self.__city_key['rbz'].values[0],
                                                      X.krs == self.__city_key['krs'].values[0],
                                                      X.gmd == self.__city_key['gmd'].values[0])

        #delete unused columns
        gebref_bearbeitet = gebref_data.drop(["lan", "rbz", "krs", "gmd"], axis = 1)

        #text encoding
        gebref_bearbeitet = gebref_bearbeitet.replace("str.", "str", regex=True).replace("Str.", "str", regex=True)\
            .replace("Ã¼", "ue", regex=True).replace("Ã¤", "ae", regex=True).replace("Ã¶", "oe", regex=True).replace("Ã", "ss", regex=True).replace(" ", "", regex=True)

        #save as a data that called gebref
        header = ["stn","hsr","adz","east","north"]
        gebref_bearbeitet.to_csv("C:/Users/Fabian Hannich/Documents/Studium/6. Semester/GI-Projekt_Immo/Hauskoordinaten_gebref_EPSG4647_ASCII/gebrefBBBB.txt", columns=header, index=False)

        return gebref_bearbeitet


    #read gebref_keys-data and assign types
    @staticmethod
    def read_keys(gebref_keys_path):
        print("Read an filter gebraf_keys-data..")
        gebref_keys = pd.read_csv(gebref_keys_path,
                                  header=None,
                                  names=['type', 'lan', 'rbz',
                                         'krs', 'gmd', 'nam'],
                                  sep=';',
                                  dtype={'type': str, 'lan': str, 'rbz': str,
                                         'krs': str, 'gmd': str, 'nam': str},
                                  encoding='utf-8')

        #filter types = G
        #gebref_keys = gebref_keys.loc[lambda df: df.type == 'G', :]
        gebref_keys = gebref_keys >> mask(X.type == 'G')

        return gebref_keys

    #filter gebref_keys from Essen
    def get_city_key(self):
        return self.gebref_keys >> mask(X.nam == self.__studyarea)

    #get Coordinates from an adress
    def getCoordinates(self, adresse, gebref):
        a = adresse.split()
        counter = len(a)

        if counter == 2:
            gebref = gebref >> mask (X.stn == a[0],
                                     X.hsr == a[1])

        else:
            gebref = gebref >> mask(X.stn == a[0],
                                    X.hsr == a[1],
                                    X.adz == a[2])

        coordinates = gebref.to_string(index=False, header = False, columns=["east","north"] ,index_names=False, decimal=',')

        return coordinates



    #Getter
    @property
    def gebref(self):
        return self.__gebref

    @property
    def gebref_keys(self):
        return self.__gebref_keys

    @property
    def city_key(self):
        return self.__city_key

    @property
    def studyarea(self):
        return self.studyarea


#datapath
geb_ref = "C:/Users/Fabian Hannich/Documents/Studium/6. Semester/GI-Projekt_Immo/Hauskoordinaten_gebref_EPSG4647_ASCII/gebref.txt"
geb_ref_keys = "C:/Users/Fabian Hannich/Documents/Studium/6. Semester/GI-Projekt_Immo/Hauskoordinaten_gebref_EPSG4647_ASCII/gebref_schluessel.txt"

#start class BuildingReferences
br = BuildingReferences(geb_ref, geb_ref_keys, 'Essen')
print(br.getCoordinates('Dilldorferstr 52 a', br.gebref))
