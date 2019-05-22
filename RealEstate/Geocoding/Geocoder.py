"""
Description: Class to get the coordinates from
            the addresses. If the address does
            not exist in the ALKIS dataset,
            you will get them about OpenStreetMap.
Author: Lena Karweg, lena.karweg@hs-bochum.de
        Fabian Hannich, fabian.hannich@hs-bochum.de
"""

import geocoder
from pyproj import Proj, transform as transform_coordinates
from dfply import *
from datetime import datetime as dt
import time
import difflib

from RealEstate.Geocoding.BuildingReferences import BuildingReferences


class Geocoder:

    # define transformation parameter
    WGS84 = Proj(init='epsg:4326')
    ETRS89 = Proj(init='epsg:4647')

    def __init__(self, gebref):
        self.gebref = gebref.data
        self.time = dt.now()

        # streets from ALKIS
        multiple_streets = self.gebref["stn"].tolist()
        self.gebref_streets = list(set(multiple_streets))

    def get_coordinates(self, street, street_house_number, house_number_supplement, city, coord_available):
        """
        Get Coordinates from an address
        """
        street = self.normalize_street(s=street)

        # street in ALKIS available
        if street not in self.gebref_streets:
            # find similar street name
            street_mod = difflib.get_close_matches(word=street,
                                                   possibilities=self.gebref_streets,
                                                   n=1,
                                                   cutoff=0.8)

            if len(street_mod) == 1:
                print("streets name has been changed: ", street, "  to  ", street_mod[0])
                street = street_mod[0]

        # build address strings for geocoding
        address_alkis, address_geocode = self.paste_address(city,
                                                            house_number_supplement,
                                                            street,
                                                            street_house_number)

        # subset ALKIS gebref
        subset_gebref = self.subset_gebref(address_elements=address_alkis)

        # address in ALKIS
        if subset_gebref.shape[0] == 1:

            x = subset_gebref['east'].values[0]
            y = subset_gebref['north'].values[0]
            accuracy = 1
            source = "ALKIS"

            return self.return_data(x=x,
                                    y=y,
                                    accuracy=accuracy,
                                    source=source)

        else:

            # coordinates in mod
            if coord_available:
                print("Coordinates in data")
                return None
            else:
                # multiple results
                if subset_gebref.shape[0] > 1:
                    print("Geocoding ALKIS multiple results")
                    print(subset_gebref)

                # geocode address
                accuracy, x, y, source = self.geocode_osm(address_geocode)

                return self.return_data(x=x,
                                        y=y,
                                        accuracy=accuracy,
                                        source=source)

    @staticmethod
    def paste_address(city, house_number_supplement, street, street_house_number):
        if house_number_supplement != "":
            address_geocode = street + ', ' + street_house_number + ' ' + house_number_supplement.lower() + ', ' + city
            address_alkis = street + ', ' + street_house_number + ', ' + house_number_supplement.lower()
        else:
            address_geocode = street + ', ' + street_house_number + ', ' + city
            address_alkis = street + ', ' + street_house_number

        return address_alkis.replace(' ', '').replace(',,', ','), address_geocode.replace(' ', '').replace(',,', ',')

    def subset_gebref(self, address_elements):
        """
        Get ALKIS entry by address
        """
        # split address
        address_elements = address_elements.split(',')
        counter = len(address_elements)

        street = self.normalize_street(address_elements[0])

        # subset gebref
        if counter == 2:
            return self.gebref >> mask(X.stn == street,
                                       X.hsr == address_elements[1],
                                       X.adz == "")

        # street, house number and supplement
        elif counter == 3:
            return self.gebref >> mask(X.stn == street,
                                       X.hsr == address_elements[1],
                                       X.adz == address_elements[2])

        # no match
        else:
            return None

    @staticmethod
    def normalize_street(s):
        """
        Normalize address
        """
        return s.replace("Strasse", "str").replace("Straße.", "str").replace("str.", "str")\
                .replace("straße.", "str").replace("straße", "str").replace("strasse.", "str")\
                .replace("str.", "str").replace("Str.", "str").replace("Ã¼", "ue").replace("Ã¤", "ae")\
                .replace("Ã¶", "oe").replace("Ã", "ss").replace(" ", "").replace("-", "")

    def geocode_osm(self, address):
        """
        Geocode address by OpenStreetMap
        """
        try:
            # query the time
            current_time = dt.now()

            # one request per second
            if self.time_difference(current_time) < 1:
                time.sleep(1)

            # geocode address
            coder_osm = geocoder.osm(address, maxRows=1)

            # set new request time
            self.time = dt.now()

            if coder_osm.ok:

                json = coder_osm.geojson['features'][0]['properties']

                # extract information
                accuracy = json['accuracy']
                lat = json['lat']
                lng = json['lng']

                # convert wgs to etrs
                x_trans, y_trans = self.wgs2etrs(lng, lat)

                return self.return_data(accuracy=accuracy,
                                        x=x_trans,
                                        y=y_trans,
                                        source="OSM")
            else:
                print("Coder not ok: ", address)
                return self.return_data()

        except ConnectionError as e:
            print("Geocoding ConnectionError: ", e)
            return self.return_data()

    @staticmethod
    def return_data(accuracy=0, x=0, y=0, source=""):
        """
        Return geocoding results
        """
        return {"x": x,
                "y": y,
                "accuracy": accuracy,
                "source": source}

    def wgs2etrs(self, lng, lat):
        """
        Transform coordinates from WGS84 to ETRS89
        """
        return transform_coordinates(p1=self.WGS84,
                                     p2=self.ETRS89,
                                     x=lng,
                                     y=lat)

    # time difference
    def time_difference(self, current_time):
        """
        Get time difference
        """
        return (current_time - self.time).total_seconds()


if __name__ == '__main__':
    br = BuildingReferences(city='Essen',
                            path='C:/Users/Kelm/Desktop/gebref')
    g = Geocoder(gebref=br)
    coord = g.get_coordinates(street='Frrintroperstraße',
                              street_house_number='432',
                              house_number_supplement='',
                              city='Essen',
                              coord_available=False)
    print(coord)
