import pandas as pd

from osm import Geocoder


class ImmoDataModel:

    def __init__(self, data):
        self.data = self.prepare_data(data)
        self.geocoder = Geocoder()


    def prepare_data(self, data):
        ## hier kommen alle Attribute hin

        # Pandas DataFrame als Datengrundlage der Klasse
        e_id = data['@id']
        street = data['address']['street'] if "street" in data['address'] else None
        street_hsno = data['address']['houseNumber'] if "houseNumber" in data['address'] else None
        zipcode = data['address']['postcode']
        city = data['address']['city']
        title = data['title']
        private_offer = data['privateOffer'].capitalize()
        rent_brutto = data['price']['value']
        rent_netto = data['calculatedPrice']['value']
        living_space = data['livingSpace']
        qm_price = rent_brutto/living_space
        num_rooms = data['numberOfRooms']
        fitted_kitchen = data['builtInKitchen'].capitalize()
        balcony = data['balcony'].capitalize()
        garden = data['garden'].capitalize()

        address = city + " " + street + " " + street_hsno
        print(address)
        coordinates = self.geocoder.geocode(address)



        verified_lat = None
        verified_long = None
        verified_x = coordinates ["x"]
        verified_y = None
        accuracy: None




        df = pd.DataFrame(
            {
                "expose_id": [e_id],
                # "address": [data['address']['street'] if "street" in data['address'] else "" + " " + data['address'][
                #     'houseNumber'] if "houseNumber" in data['address'] else "" + ", " +
                #                                                             data['address']['postcode'] + " " +
                #                                                             data['address']['city']],
                "street": [street],
                "street_hsno": [street_hsno],
                "zipcode": [zipcode],
                "city": [city],
                "title": [title],
                "private_offer": [private_offer],
                "rent_brutto_eur": [rent_brutto],
                "rent_netto_eur": [rent_netto],
                "living_space": [living_space],
                "qm_price": [qm_price],
                "num_rooms": [num_rooms],
                "fitted_kitchen": [fitted_kitchen],
                "balcony": [balcony],
                "garden": [garden],

                #"verified_address": None,
                "verified_lat": [verified_lat],
                "verified_long": [verified_long],
                "verified_x": [verified_x],
                "verified_y": [verified_y],
                "accuracy": [accuracy],

            }
        )

        return df.astype(dtype={"expose_id": "int64",
                                        # "address": "str",
                                        "street": "str",
                                        "street_hsno": "str",
                                        "zipcode": "str",  # Because it always has to have 5 digits
                                        "city": "str",
                                        "title": "str",
                                        "private_offer": "bool",
                                        "rent_brutto": "float",
                                        "rent_netto": "float",
                                        "living_space": "float",
                                        "num_rooms": "float",
                                        "fitted_kitchen": "bool",
                                        "balcony": "bool",
                                        "garden": "bool",

                                        # "verified_address": "str",
                                        "verified_lat": "float64",
                                        "verified_long": "float64",
                                        "accuracy": "float",

                                        })


    @property
    def get_data(self):
        return self.data


