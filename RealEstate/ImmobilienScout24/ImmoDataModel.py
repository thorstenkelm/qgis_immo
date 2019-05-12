"""
Description: # TODO class description is missing
Author: Marlena Hecker, marlena.hecker@hs-bochum.de
"""

import pandas as pd
from RealEstate.Geocoding.Geocoder import Geocoder

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

        #information of expose
        expose_id = self.get_element('@id')
        title = self.get_element('resultlist.realEstate_title')
        private_offer = self.string_2_bool(self.get_element('resultlist.realEstate_privateOffer'))

        #address
        street = self.get_element('resultlist.realEstate_address_street')
        street_hsno = self.get_element('resultlist.realEstate_address_houseNumber')
        zipcode = self.get_element('resultlist.realEstate_address_postcode')
        city = self.get_element('resultlist.realEstate_address_city')

        #rent
        rent_brutto_eur = self.get_element('resultlist.realEstate_price_value')
        # rent_brutto_marketing_type = self.get_element('resultlist.realEstate_marketingType')
        # rent_brutto_interval_type = self.get_element('resultlist.realEstate_price_priceIntervalType')
        rent_netto_eur = self.get_element('resultlist.realEstate_calculatedPrice_value')
        # rent_netto_marketing_type = self.get_element('resultlist.realEastate_calculatedPrice_marketingType')
        # rent_netto_interval_type = self.get_element('resultlist.realEastate_calculatedPrice_priceIntervalType')
        rent_scope = self.get_element('resultlist.realEastate_calculatedPrice_rentScope')
        heating_costs = self.get_element('obj_heatingCosts')

        #characteristics of a real estate
        living_space_sqm = self.get_element('resultlist.realEstate_livingSpace')
        sqm_price = float(rent_brutto_eur) / float(living_space_sqm)
        num_rooms = self.get_element('resultlist.realEstate_numberOfRooms')
        fitted_kitchen = self.string_2_bool(self.get_element('resultlist.realEstate_builtInKitchen'))
        balcony = self.string_2_bool(self.get_element('resultlist.realEstate_balcony'))
        garden = self.string_2_bool(self.get_element('resultlist.realEstate_garden'))
        cellar = self.string_2_bool(self.get_element('obj_cellar'))
        lift = self.string_2_bool(self.get_element('obj_lift'))
        fully_accessible = self.string_2_bool(self.get_element('obj_barrierFree')) #Barrierefrei
        assisted_living = self.string_2_bool(self.get_element('obj_assistedLiving')) #betreutes Wohnen
        object_state = self.get_element('obj_condition') #Objektzustand
        floor = self.get_element('obj_floor')
        firing_type = self.get_element('obj_firingType')
        heating_type = self.get_element('obj_heatingType')
        realestate_type = self.get_element('obj_immotype')
        interior_quality = self.get_element('obj_interiorQual')
        flat_type = self.get_element('obj_typeOfFlat')
        year_construction = self.get_element('obj_yearConstructed')
        last_refurbish = self.get_element('obj_lastRefurbish')


        data_dict = {
            "expose_id": [expose_id],
            "street": [street],
            "street_hsno": [street_hsno],
            "zipcode": [zipcode],
            "city": [city],
            "title": [title],
            "private_offer": [private_offer],
            "rent_brutto_eur": [rent_brutto_eur],
            # "rent_brutto_marketing_type" : rent_brutto_marketing_type,
            # "rent_brutto_interval_type" : # rent_brutto_interval_type,
            "rent_netto_eur": [rent_netto_eur],
            # "rent_netto_marketing_type" : rent_netto_marketing_type],
            # "rent_netto_interval_type" : rent_netto_interval_type],
            "rent_scope": [rent_scope],
            "living_space": [living_space_sqm],
            "sqm_price": sqm_price,
            "num_rooms": [num_rooms],
            "fitted_kitchen": [fitted_kitchen],
            "balcony": [balcony],
            "garden": [garden],
            "cellar": [cellar],
            "lift": [lift],
            "fully_accessible": [fully_accessible],
            "assisted_living": [assisted_living],
            "object_state": [object_state],
            "floor": [floor],
            "firing_type": [firing_type],
            "heating_type": [ heating_type],
            "realestate_type": [realestate_type],
            "interior_quality": [interior_quality],
            "flat_type": [flat_type],
            "year_construction": [year_construction],
            "last_refurbish": [last_refurbish],
            "heating_costs": [heating_costs]

         }

        return pd.DataFrame(data_dict)

    def get_element(self, key):
        """
        TODO description is missing
        :param key: str
        :return: value
        """
        try:
            if isinstance(self.init_data.get(key), pd.Series):
                return self.init_data.get(key).values[0]
            elif isinstance(self.init_data.get(key), pd.DataFrame):
                return self.init_data.get(key).values[0]
            else:
                return self.init_data.get(key)

        except KeyError as e:
            print(key)
            print(e)
            # no element in data
            # return empty string
            return ''
        except AttributeError as e:
            print(key)
            print(e)
            return ''

    def string_2_bool(self, value):
        return value.lower() in ("y", "true")

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
                                    #"sqm_price": "float",
                                    "num_rooms": "float",
                                    "fitted_kitchen": "bool",
                                    "balcony": "bool",
                                    "garden": "bool",
                                    "cellar": "bool",
                                    "lift": "bool",
                                    "fully_accessible": "bool",
                                    "assisted_living": "bool",
                                    "object_state": "str",
                                    "floor": "int",
                                    "firing_type": "str",
                                    "heating_type": "str",
                                    "realestate_type": "str",
                                    "interior_quality": "str",
                                    "flat_type": "str",
                                    "year_construction": "int",
                                    "last_refurbish": "int",
                                    "heating_costs": "float"
                                    })
        except ValueError as e:
            print(e)


    @property
    def get_data(self):
        return self.data


    def get_address(self):
        """
        Return address (e.g. for geocoder)
        :return:
        """
        return self.data["street"].values[0] + " " + self.data["street_hsno"].values[0]


    def set_coordinates(self, coordinates):
        """
        Set coordinates from geocoder
        :param coordinates: dict (accuracy, lat, lon, x, y)
        """

        self.data = self.data.assign(x=coordinates.get("x"))
        self.data = self.data.assign(y=coordinates.get("y"))
        self.data = self.data.assign(accuracy=coordinates.get("accuracy"))
