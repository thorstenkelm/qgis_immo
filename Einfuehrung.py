#!/usr/bin/env python                               # Symbolisiert dem Betriebssystem, mit welchem Interpreter die Datei ausgeführt werden kann.
# -*- coding: utf-8 -*-                             # Datei ist im UTF-8 Format encodiert

import pandas as pd

class ImmobilienScout:                              # Definition der Klasse

    IS24_URL = 'https://www.immobilienscout24.de'   # Konstante Klassenvariable

    def __init__(self, url, stadt, datei_name):
        """

        :param url:
        :param stadt:
        :param datei_name:
        """
        self.url = url                              # Klassenvariable - public
        self._stadt = stadt                         # Klassenvariable - protected
        self.__datei_name = datei_name              # Klassenvariable - private

    def execute(self):                              # Hauptmethode zur ausfuehrung
        '''
        Dies ist die Hauptmethode
        :return: None
        '''
        str_stadt = self.get_city_str()             # Aufruf Methode get_city_str
        print(str_stadt)


    def get_city_str(self):
        '''

        :return:
        '''
        return "Stadt: " + self._stadt

    @property                                       # Beschreibt Methode als Getter
    def url(self):                                  # Getter Methode URL
        return self.url()                           # Unnoetig, da URL public :-)

    @url.setter                                     # Setter Methode
    def url(self, value):
        self._url = value

    @property
    def stadt(self):                                # Getter Methode Stadt
        return self._stadt()

    @property
    def datei_name(self):                           # Getter Methode Datei Name
        return self.__datei_name()




i = ImmobilienScout(url="Testurl",
                    stadt="Teststadt",
                    datei_name="lokaledatei.csv")

i.execute()