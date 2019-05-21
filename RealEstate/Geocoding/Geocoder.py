"""
Description: Class to get the coordinates from
            the addresses. If the address does
            not exist in the ALKIS dataset,
            you will get them about OpenStreetMap.
Author: Lena Karweg, lena.karweg@hs-bochum.de
        Fabian Hannich, fabian.hannich@hs-bochum.de
"""

import geocoder
from pyproj import Proj, transform
from dfply import *
from datetime import datetime as DateTime
import time
from RealEstate.Geocoding.BuildingReferences import BuildingReferences


class Geocoder:
    # define transformation parameter
    WGS84 = Proj(init='epsg:4326')
    ETRS89 = Proj(init='epsg:4647')

    def __init__(self, gebref):
        self.__gebref = gebref
        self.__time = DateTime.now().strftime('%H:%M:%S')

    # get coordinates from an address
    def get_coordinates(self, address):
        gebref = self.__search_address(address)

        if gebref.empty == True:
            return self.__geocode(address)

        elif gebref.shape[0] == 1:
            coordinates = gebref.to_dict(orient='list')
            y = coordinates['east']
            x = coordinates['north']
            accuracy = 1

            return self.__return_data(accuracy=accuracy,
                                      x=x,
                                      y=y)

        else:
            return self.__geocode(address)

    def __search_address(self, address):
        a = address.split()
        counter = len(a)

        if counter == 2:
            gebref = self.__gebref >> mask(X.stn == a[0],
                                           X.hsr == a[1])
            return gebref

        elif counter == 3:
            gebref = self.__gebref >> mask(X.stn == a[0],
                                           X.hsr == a[1],
                                           X.adz == a[2])
            return gebref

        else:
            return self.__gebref

    def __geocode(self, address):

        try:
            # query the time
            current_time = DateTime.now().strftime('%H:%M:%S')

            if self.__time_difference(current_time) < 1:
                 time.sleep(1000)

            # set time
            self.time(current_time)

            # geocode address
            g = geocoder.osm(address)

            if g.ok:

                json = g.geojson['features'][0]['properties']

                # extract information
                accuracy = json['accuracy']
                lat = json['lat']
                lng = json['lng']

                # convert wgs to etrs
                x_trans, y_trans = self.__wgs2etrs(lng, lat)

                return self.__return_data(accuracy=accuracy,
                                          x=x_trans,
                                          y=y_trans)
            else:
                return self.__return_data()


        except ConnectionError as e:
            print(e)
            return self.__return_data()

    @staticmethod
    def __return_data(accuracy=0, x=0, y=0):
        return {"accuracy": accuracy,
                "x": x,
                "y": y}

    def __wgs2etrs(self, lng, lat):
        """

        :param lng: longitude
        :param lat: latitude
        :return: x, y
        """
        return transform(self.WGS84, self.ETRS89, lng, lat)

    # getter time
    @property
    def time(self):
        return self.__time

    # setter time
    @time.setter
    def time(self, value):
        self.__time = value

    #time difference
    def __time_difference(self, time):
        return time - self.time

if __name__ == '__main__':
    br = BuildingReferences(city='Essen',
                            path='C:/gebref')
    g = Geocoder(br.gebref)
    print(g.get_coordinates("Witteringstr 9"))
