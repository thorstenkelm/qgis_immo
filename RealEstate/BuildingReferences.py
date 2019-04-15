# -*- coding: utf-8 -*-
# Author: Thorsten Kelm, thorsten.kelm@hs-bochum.de

from dfply import *


class BuildingReferences:

    def __init__(self, gebref_path, gebref_keys_path, studyarea):
        self.__studyarea = studyarea
        self.__gebref_keys = self.read_keys(gebref_keys_path)
        self.__city_key = self.get_city_key()
        self.__gebref = self.read_data(gebref_path)

    def read_data(self, gebref_path):
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
        gebref_data.fillna('', inplace=True)

        gebref_data = gebref_data >> mask(X.lan == self.__city_key['lan'].values[0],
                                          X.rbz == self.__city_key['rbz'].values[0],
                                          X.krs == self.__city_key['krs'].values[0],
                                          X.gmd == self.__city_key['gmd'].values[0])

        return gebref_data

    @staticmethod
    def read_keys(gebref_keys_path):
        gebref_keys = pd.read_csv(gebref_keys_path,
                                  header=None,
                                  names=['type', 'lan', 'rbz',
                                         'krs', 'gmd', 'nam'],
                                  sep=';',
                                  dtype={'type': str, 'lan': str, 'rbz': str,
                                         'krs': str, 'gmd': str, 'nam': str},
                                  encoding='utf-8')

        # gebref_keys = gebref_keys.loc[lambda df: df.type == 'G', :]
        gebref_keys = gebref_keys >> mask(X.type == 'G')

        return gebref_keys

    def get_city_key(self):
        return self.gebref_keys >> mask(X.nam == self.__studyarea)

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


geb_ref = "..Data/gebref.txt"
geb_ref_keys = "..Data/gebref_schluessel.txt"

br = BuildingReferences(geb_ref, geb_ref_keys, 'Essen')
print(br.gebref)
