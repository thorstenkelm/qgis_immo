# -*- coding: utf-8 -*-
"""
Class for the provision of ALKIS house coordinates in NRW
Author: Fabian Hannich, fabian.hannich@hs-bochum.de
"""


import urllib.request
import zipfile
from dfply import *
from pathlib import Path


class BuildingReferences:

    GEBREF_URL = 'https://www.opengeodata.nrw.de/produkte/geobasis/lika/alkis_sek/gebref/gebref_EPSG4647_ASCII.zip'
    COLUMNS = ['stn', 'hsr', 'adz', 'east', 'north', ]

    def __init__(self, city, path):
        self.path = path
        self.city = city

        self.gebref_zip_path = path + '/gebref_EPSG4647_ASCII.zip'
        self.gebref_path = path + '/gebref.txt'
        self.gebref_key_path = path + '/gebref_schluessel.txt'
        self.gebref_city_path = path + '/' + city + '.csv'

        # Gebref city is available
        if Path(self.gebref_city_path).is_file():
            # import city_gebref
            self.gebref = self.read_city_gebref()

        # Gebref ALKIS is not available
        elif not Path(self.gebref_zip_path).is_file():
                # download gebref raw file
                self.download_data()

        else:
            # get keys
            self.gebref_keys = self.read_keys()
            self.city_key = self.get_city_key()

            # import data
            raw_gebref = self.read_raw_gebref()

            # subset data
            city_gebref = self.subset_gebref(gebref=raw_gebref)
            city_gebref = self.select_col(gebref=city_gebref)
            self.gebref = self.transform_address(gebref=city_gebref)

            # export data to file system
            self.gebref2csv()

    def download_data(self):
        try:
            print("Download ALKIS data...")
            urllib.request.urlretrieve(url=self.GEBREF_URL,
                                       filename=self.gebref_zip_path)
            print("Unpack file...")
            zipfile.ZipFile(file=self.gebref_zip_path).extractall(self.path)
        except Exception as e:
            print('Download data: ' + str(e))

    def read_keys(self):
        """
        Get keys from gebref
        """
        gebref_keys = pd.read_csv(self.gebref_key_path,
                                  header=None,
                                  names=['type', 'lan', 'rbz',
                                         'krs', 'gmd', 'nam'],
                                  sep=';',
                                  dtype={'type': str, 'lan': str, 'rbz': str,
                                         'krs': str, 'gmd': str, 'nam': str},
                                  encoding='utf-8')

        # filter types
        return gebref_keys >> mask(X.type == 'G')

    def get_city_key(self):
        """
        Get key from given city
        """
        return self.gebref_keys >> mask(X.nam == self.city)

    def subset_gebref(self, gebref):
        """
        Subset gebref by given city key
        """
        return gebref >> mask(X.lan == self.city_key['lan'].values[0],
                              X.rbz == self.city_key['rbz'].values[0],
                              X.krs == self.city_key['krs'].values[0],
                              X.gmd == self.city_key['gmd'].values[0])

    def select_col(self, gebref):
        """
        Subset columns of gebref
        """
        return gebref >> select(self.COLUMNS)

    def read_raw_gebref(self):
        """
        Read raw gebref file from file system
        """
        gebref_data = pd.read_csv(self.gebref_path,
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

        # fill empty lines
        gebref_data.fillna('', inplace=True)
        return gebref_data

    def read_city_gebref(self):
        gebref_data = pd.read_csv(self.gebref_city_path,
                                  sep=',',
                                  decimal='.',
                                  header=0,
                                  names=['lan', 'rbz', 'krs', 'gmd', 'hsr',
                                         'adz', 'east', 'north', 'stn'],
                                  dtype={'lan': str, 'rbz': str, 'krs': str, 'gmd': str, 'hsr': str,
                                         'adz': str, 'east': float, 'north': float, 'stn': str},
                                  encoding='ISO-8859-1')

        # fill empty lines
        gebref_data.fillna('', inplace=True)
        return gebref_data

    @staticmethod
    def transform_address(gebref):
        return gebref.replace("str.", "str", regex=True)\
            .replace("Str.", "str", regex=True) \
            .replace("Ã¼", "ue", regex=True) \
            .replace("Ã¤", "ae", regex=True) \
            .replace("Ã¶", "oe", regex=True) \
            .replace("Ã", "ss", regex=True) \
            .replace(" ", "", regex=True)

    def gebref2csv(self):
        """
        Save as a data that called gebref
        """
        self.gebref.to_csv(self.gebref_city_path,
                           index=False,
                           sep=';',
                           decimal='.')


if __name__ == '__main__':
    br = BuildingReferences(city='Essen',
                            path='C:/gebref')

    print(br.gebref)
