"""
Description: # TODO class description is missing
Author: Marlena Hecker, marlena.hecker@hs-bochum.de
"""


class ImmoDataModel:

    def __init__(self, data):
        self.init_data = data
        self.data = self.prepare_data()

    def prepare_data(self):
        """
        # TODO description is missing
        :param data: Pandas DataFrame or Dict
        :return:
        """
        # extract data
        expose_id = self.get_element('@id')
        street = self.get_element('resultlist.realEstate_address_street')
        street_hsno = self.get_element('resultlist.realEstate_address_houseNumber')

        # e_id = data['@id']
        # street = data['address']['street'] if "street" in data['address'] else None
        # street_hsno = data['address']['houseNumber'] if "houseNumber" in data['address'] else None
        # zipcode = data['address']['postcode']
        # city = data['address']['city']
        # title = data['title']
        # private_offer = data['privateOffer'].capitalize()
        # rent_brutto = data['price']['value']
        # rent_netto = data['calculatedPrice']['value']
        # living_space = data['livingSpace']
        # qm_price = rent_brutto/living_space
        # num_rooms = data['numberOfRooms']
        # fitted_kitchen = data['builtInKitchen'].capitalize()
        # balcony = data['balcony'].capitalize()
        # garden = data['garden'].capitalize()
        #
        # address = city + " " + street + " " + street_hsno
        # print(address)

        #
        #
        #
        # df = pd.DataFrame(
        #     {
        #         "expose_id": [e_id],
        #         # "address": [data['address']['street'] if "street" in data['address'] else "" + " " + data['address'][
        #         #     'houseNumber'] if "houseNumber" in data['address'] else "" + ", " +
        #         #                                                             data['address']['postcode'] + " " +
        #         #                                                             data['address']['city']],
        #         "street": [street],
        #         "street_hsno": [street_hsno],
        #         "zipcode": [zipcode],
        #         "city": [city],
        #         "title": [title],
        #         "private_offer": [private_offer],
        #         "rent_brutto_eur": [rent_brutto],
        #         "rent_netto_eur": [rent_netto],
        #         "living_space": [living_space],
        #         "qm_price": [qm_price],
        #         "num_rooms": [num_rooms],
        #         "fitted_kitchen": [fitted_kitchen],
        #         "balcony": [balcony],
        #         "garden": [garden],
        #
        #         #"verified_address": None,
        #         "verified_lat": [verified_lat],
        #         "verified_long": [verified_long],
        #         "verified_x": [verified_x],
        #         "verified_y": [verified_y],
        #         "accuracy": [accuracy],
        #
        #     }
        # )
        #
        # return

    def get_element(self, key):
        """
        TODO description is missing
        :param key: str
        :return: value
        """
        try:
            return self.init_data.get(key).values[0]
        except KeyError as e:
            print(e)
            # no element in data
            # return empty string
            return ''
        except AttributeError as e:
            print(e)
            return ''

    def set_type(self):
        """
        Set type of data
        :return:
        """
        try:
            # set type
            # self.data.astype(dtype={"expose_id": "int64",
            #                                 # "address": "str",
            #                                 "street": "str",
            #                                 "street_hsno": "str",
            #                                 "zipcode": "str",  # Because it always has to have 5 digits
            #                                 "city": "str",
            #                                 "title": "str",
            #                                 "private_offer": "bool",
            #                                 "rent_brutto": "float",
            #                                 "rent_netto": "float",
            #                                 "living_space": "float",
            #                                 "num_rooms": "float",
            #                                 "fitted_kitchen": "bool",
            #                                 "balcony": "bool",
            #                                 "garden": "bool",
            #
            #                                 # "verified_address": "str",
            #                                 "verified_lat": "float64",
            #                                 "verified_long": "float64",
            #                                 "accuracy": "float",
            #
            #                                 })
            pass
        except ValueError as e:
            print(e)

    @property
    def get_data(self):
        return self.data

    def get_address(self):
        """
        Get address from geocoder
        :return:
        """
        pass

    def set_coordinates(self, coordinates):
        """
        Set coordinates from geocoder
        :param coordinates: dict (accuracy, lat, lon, x, y)
        """

        # coordinates = self.geocoder.geocode(address)
        #
        #
        #
        # verified_lat = None
        # verified_long = None
        # verified_x = coordinates ["x"]
        # verified_y = None
        # accuracy: None

        pass
