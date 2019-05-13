"""
Description: # TODO class description is missing
Author: Lena Karweg, lena.karweg@hs-bochum.de
"""

import geocoder
from pyproj import Proj, transform
from dfply import *


class Geocoder():
    # define transformation parameter
    WGS84 = Proj(init='epsg:4326')
    ETRS89 = Proj(init='epsg:4647')

    def __init__(self, gebref):
        self.__gebref = gebref
        

    # get Coordinates from an adress
    def getCoordinates(self, address):
        a = address.split()
        counter = len(a)

        if counter == 2:
            gebref = self.gebref >> mask(X.stn == a[0],
                                         X.hsr == a[1])

        elif counter == 3:
            gebref = self.gebref >> mask(X.stn == a[0],
                                         X.hsr == a[1],
                                         X.adz == a[2])

        else:
            print("Geocode-function is used to get the coordinates..")
            return self.geocode(address)

            coordinates = gebref.to_dict(orient='list')
            x = coordinates['east']
            y = coordinates['north']
            accuracy = 1

            return {"accuracy": accuracy,
                    "x": x,
                    "y": y}

    def geocode(self, address):

        # TODO "try-block" no address found - https://geocoder.readthedocs.io/api.html#examples Error Handling
        # TODO try-block ConnectionError - return is missing
        try:
            #Uhrzeitabfrage
            # geocode address
            g = geocoder.osm(address)
            if g.ok:

                json = g.geojson['features'][0]['properties']

                # extract information
                accuracy = json['accuracy']
                lat = json['lat']
                lng = json['lng']

                # convert wgs to etrs
                x_trans, y_trans = self.wgs2etrs(lng, lat)

                return self.return_data(accuracy,
                                        x_trans,
                                        y_trans)
            else:
                return self.return_data()


        except ConnectionError as e:
            print(e)
            return self.return_data()

    @staticmethod
    def return_data(accuracy=0, x=0, y=0):
        return {"accuracy": accuracy,
                "x": x,
                "y": y}

    def wgs2etrs(self, lng, lat):
        """

        :param lng:
        :param lat:
        :return:
        """
        return transform(self.WGS84, self.ETRS89, lng, lat)

if __name__ == '__main__':
    # g = Geocoder(gebref=, adresse="Witteringstr 9")
    pass
