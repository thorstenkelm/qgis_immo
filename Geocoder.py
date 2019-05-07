import geocoder
from pyproj import Proj, transform
from dfply import *

class Geocoder:

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


    def geocode(self, adresse):
        g = geocoder.osm(adresse)

        l = g.geojson['features'][0]['properties']

        accaracy = l['accuracy']
        lat = l['lat']
        lng =l['lng']
        x_trans, y_trans = self.WGS2ETRS(lng, lat)
        return {"accaracy" : accaracy,
               "latitude" : lat,
               "longitude" : lng,
               "x": x_trans,
               "y": y_trans}


    def WGS2ETRS(self, lng, lat):
        x_trans, y_trans = transform(self.WGS84, self.ETRS89, lng, lat)
        return  x_trans, y_trans


adress = "Essen Witteringstr 9 "
n = Geocoder(adress)

print(n.geocode(adress)['x'],n.geocode(adress)['y'])


#Funktion getCoordinate in Geocoder kopieren
#accaracy auf 1 setzen bei den Hauskoordinaten
#keine Adresse gefunden = NONE
