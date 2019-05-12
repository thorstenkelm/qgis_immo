"""
Description: # TODO class description is missing
Author: Lena Karweg, lena.karweg@hs-bochum.de
"""

import geocoder
from pyproj import Proj, transform
from dfply import *

class Geocoder ():

    # define transformation parameter
    WGS84 = Proj(init='epsg:4326')
    ETRS89 = Proj(init='epsg:4647')

    def __init__(self, gebref, adresse):
        self.__gebref = gebref
        self.__adresse = adresse


    # get Coordinates from an adress
    def getCoordinates(self, adresse):
        a = adresse.split()
        counter = len(a)

        try:
            if counter == 2:
                gebref = self.gebref >> mask(X.stn == a[0],
                                         X.hsr == a[1])

            if counter == 3:
                gebref = self.gebref >> mask(X.stn == a[0],
                                         X.hsr == a[1],
                                         X.adz == a[2])


            coordinates = gebref.to_dict(orient='list')
            x = coordinates['east']
            y = coordinates['north']
            accuracy = 1

            return {"accuracy": accuracy,
                    "x": x,
                    "y": y}

        except:
            print("Geocode-function is used to get the coordinates..")
            return self.geocode(adresse)



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
    g = Geocoder(gebref=, adresse="Witteringstr 9")


