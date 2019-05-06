import geocoder
from pyproj import Proj, transform

class Geocoder:

    WGS84 = Proj(init='epsg:4326')
    ETRS89 = Proj(init='epsg:4647')

    def __init__(self, adresse):
        self.__adresse = adresse

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

print(n.geocode(adress))
