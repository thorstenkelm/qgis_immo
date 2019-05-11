"""
Description: # TODO class description is missing
Author: Marlena Hecker, marlena.hecker@hs-bochum.de
"""

import pandas as pd


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
        zipcode = self.get_element('resultlist.realEstate_address_postcode')
        city = self.get_element('resultlist.realEstate_city')
        title = self.get_element('resultlist.realEstate_title')
        private_offer = self.get_element('resultlist.realEstate_title').capitilize()
        rent_brutto_eur = self.get_element('resultlist.realEstate_price_value')
        # rent_brutto_marketing_type = self.get_element('resultlist.realEstate_marketingType')
        # rent_brutto_interval_type = self.get_element('resultlist.realEstate_price_priceIntervalType')
        rent_netto_eur = self.get_element('resultlist.realEstate_calculatedPrice_value')
        # rent_netto_marketing_type = self.get_element('resultlist.realEastate_calculatedPrice_marketingType')
        # rent_netto_interval_type = self.get_element('resultlist.realEastate_calculatedPrice_priceIntervalType')
        rent_scope = self.get_element('resultlist.realEastate_calculatedPrice_rentScope')
        living_space_sqm = self.get_element('resultlist.realEstate_livingSpace')
        sqm_price = rent_brutto_eur / living_space_sqm
        num_rooms = self.get_element('resultlist.realEstate_numberOfRooms')
        fitted_kitchen = self.get_element('resultlist.realEstate_builtInKitchen').capitalize()
        balcony = self.get_element('resultlist.realEstate_balcony').capitalize()
        garden = self.get_element('resultlist.realEstate_garden').capitalize()

        data_dict = {
            "expose_id": expose_id,
            "street": street,
            "street_hsno": street_hsno,
            "zipcode": zipcode,
            "city": city,
            "title": title,
            "private_offer": private_offer,
            "rent_brutto_eur": rent_brutto_eur,
            # "rent_brutto_marketing_type" : rent_brutto_marketing_type,
            # "rent_brutto_interval_type" : # rent_brutto_interval_type,
            "rent_netto_eur": rent_netto_eur,
            # "rent_netto_marketing_type" : rent_netto_marketing_type,
            # "rent_netto_interval_type" : rent_netto_interval_type,
            "rent_scope": rent_scope,
            "living_space": living_space_sqm,
            "sqm_price": sqm_price,
            "num_rooms": num_rooms,
            "fitted_kitchen": fitted_kitchen,
            "balcony": balcony,
            "garden": garden,
        }

        return pd.DataFrame(data_dict)

    def get_element(self, key):
        """
        TODO description is missing
        :param key: str
        :return: value
        """
        try:
            if self.init_data.get(key) == dict:
                return self.init_data.get(key)
            elif self.init_data.get(key) == pandas.core.frame.DataFrame or self.init_data.get(key) == pandas.core.series.Series:
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
            self.data.astype(dtype={"expose_id": "int64",
                                    "street": "str",
                                    "street_hsno": "str",
                                    "zipcode": "str",  # Because it always has to have 5 digits
                                    "city": "str",
                                    "title": "str",
                                    "private_offer": "bool",
                                    "rent_brutto_eur": "float",
                                    #"rent_brutto_marketing_type": "str",
                                    #"rent_brutto_interval_type": "str",
                                    "rent_netto_eur": "float",
                                    #"rent_netto_marketing_type": "str",
                                    #"rent_netto_interval_type": "str",
                                    "rent_scope": "str",
                                    "living_space": "float",
                                    "sqm_price": "float",
                                    "num_rooms": "float",
                                    "fitted_kitchen": "bool",
                                    "balcony": "bool",
                                    "garden": "bool"
                                    })
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
