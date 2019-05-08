"""
Description: # TODO class description is missing
Author: Lena Karweg, lena.karweg@hs-bochum.de
"""

import geocoder
from pyproj import Proj, transform
from dfply import *

class Geocoder:
    # define transformation parameter
    WGS84 = Proj(init='epsg:4326')
    ETRS89 = Proj(init='epsg:4647')

    def __init__(self, gebref):
        self.__gebref = gebref


    #get Coordinates from an adress
    def getCoordinates(self, adresse):
        a = adresse.split()
        counter = len(a)

        if counter == 2:
            gebref = self.gebref >> mask(X.stn == a[0],
                                     X.hsr == a[1])

        else:
            gebref = self.gebref >> mask(X.stn == a[0],
                                    X.hsr == a[1],
                                    X.adz == a[2])

        coordinates = gebref.to_string(index=False, header = False, columns=["east","north"] ,index_names=False, decimal=',')

        return coordinates

    # Funktion getCoordinate in Geocoder kopieren
    # accaracy auf 1 setzen bei den Hauskoordinaten
    # keine Adresse gefunden = NONE

    def geocode(self, address):

        # TODO "try-block" no address found - https://geocoder.readthedocs.io/api.html#examples Error Handling
        # TODO try-block ConnectionError - return is missing

        # geocode address
        g = geocoder.osm(address)
        json = g.geojson['features'][0]['properties']

        # extract information
        accuracy = json['accuracy']
        lat = json['lat']
        lng = json['lng']

        # convert wgs to etrs
        x_trans, y_trans = self.wgs2etrs(lng, lat)

        return {"accuracy": accuracy,
                "latitude": lat,
                "longitude": lng,
                "x": x_trans,
                "y": y_trans}

    def wgs2etrs(self, lng, lat):
        x_trans, y_trans = transform(self.WGS84, self.ETRS89, lng, lat)
        return x_trans, y_trans


if __name__ == '__main__':
    g = Geocoder()
    print(g.geocode("Essen Witteringstr 9 "))


