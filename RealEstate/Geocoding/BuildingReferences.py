# -*- coding: utf-8 -*-
# Author: Thorsten Kelm, thorsten.kelm@hs-bochum.de

import urllib.request
import zipfile
from dfply import *
from pathlib import Path



class BuildingReferences:

    GEBREF_URL = 'https://www.opengeodata.nrw.de/produkte/geobasis/lika/alkis_sek/gebref/gebref_EPSG4647_ASCII.zip'

    def __init__(self, gebref_path, gebref_keys_path, studyarea, savepath):
        self.savepath = savepath
        self.download_data()
        self.__studyarea = studyarea
        self.__gebref_keys = self.read_keys(gebref_keys_path)
        self.__city_key = self.get_city_key()
        self.__gebref = self.read_data(gebref_path)


    def download_data (self):
        gebref_file = Path(self.savepath+'/gebref.txt')
        if gebref_file.is_file():
            print("The gebref-file already exists!")

        else:
            print("Beginning file download...")
            urllib.request.urlretrieve(self.GEBREF_URL, self.savepath+'gebref.zip')
            print("..download ends!")
            print("Unpack data...")
            zipfile.ZipFile(self.savepath+'/gebref.zip', 'r').extractall(self.savepath)
            print("Data ready!")


    #read gebref-data and assign type
    def read_data(self, gebref_path):

        gebref_edit = Path(self.savepath+'/gebref_edit.txt')
        if gebref_edit.is_file():
            print("The gebref_edit-file already exists!")

            gebref_bearbeitet = pd.read_csv(gebref_edit,
                                            sep=';',
                                            decimal=',',
                                            header=None,
                                            names=['lan', 'rbz', 'krs', 'gmd', 'hsr',
                                                   'adz', 'east', 'north', 'stn'],
                                            dtype={'lan': str, 'rbz': str, 'krs': str, 'gmd': str, 'hsr': str,
                                                   'adz': str, 'east': float, 'north': float, 'stn': str},
                                            encoding='ISO-8859-1')


        else:
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

            #text encoding
            gebref_bearbeitet = gebref_data.replace("str.", "str", regex=True).replace("Str.", "str", regex=True)\
                .replace("Ã¼", "ue", regex=True).replace("Ã¤", "ae", regex=True).replace("Ã¶", "oe", regex=True).replace("Ã", "ss", regex=True).replace(" ", "", regex=True)

            #save as a data that called gebref
            gebref_bearbeitet.to_csv(self.savepath+'/gebref_edit.txt', index=False)

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
br = BuildingReferences(gebref_path=geb_ref,
                        gebref_keys_path=geb_ref_keys,
                        studyarea='Essen',
                        savepath='C:/Users/Fabian Hannich/Documents/Studium/6. Semester/GI-Projekt_Immo/Hauskoordinaten_gebref_EPSG4647_ASCII/')
