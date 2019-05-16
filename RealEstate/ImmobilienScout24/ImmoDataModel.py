"""
Description:  Data model for uniform storage of the scraped data of Immobilienscout24 webpage
Author: Marlena Hecker, marlena.hecker@hs-bochum.de
"""

import pandas as pd


class ImmoDataModel:

    def __init__(self, data):
        self.init_data = data
        self.data = self.prepare_data()
        self.set_type()

    def prepare_data(self):
        """
        Extracts relevant data from the input data
        :param data: pandas.DataFrame or Dict
        :return: pandas.DataFrame
            It returns a pandas.DataFrame, which contains the unified data of the scraper
        """
        # extract data

        # information of expose
        # date_start = self.get_element('@creation')
        expose_id = self.get_element('@id')
        title = self.get_element('resultlist.realEstate_title')
        private_offer = self.string_2_bool(self.get_element('resultlist.realEstate_privateOffer'))

        # address
        street = self.get_element('resultlist.realEstate_address_street')
        street_hsno = self.get_element('resultlist.realEstate_address_houseNumber')
        postcode = self.get_element('resultlist.realEstate_address_postcode')
        city = self.get_element('resultlist.realEstate_address_city')

        # rent
        rent_gross_eur = self.get_element('resultlist.realEstate_price_value')
        rent_gross_marketing_type = self.get_element('resultlist.realEstate_price_marketingType')
        rent_gross_interval_type = self.get_element('resultlist.realEstate_price_priceIntervalType')
        rent_net_eur = self.get_element('resultlist.realEstate_calculatedPrice_value')
        rent_net_marketing_type = self.get_element('resultlist.realEstate_calculatedPrice_marketingType')
        rent_net_interval_type = self.get_element('resultlist.realEstate_calculatedPrice_priceIntervalType')
        rent_scope = self.get_element('resultlist.realEstate_calculatedPrice_rentScope')
        heating_costs = self.get_element('obj_heatingCosts')

        # characteristics of a real estate
        living_space_sqm = self.get_element('resultlist.realEstate_livingSpace')
        sqm_price = float(rent_gross_eur) / float(living_space_sqm)
        num_rooms = self.get_element('resultlist.realEstate_numberOfRooms')
        num_parking_spaces = self.get_element("obj_noParkSpaces")
        fitted_kitchen = self.string_2_bool(self.get_element('resultlist.realEstate_builtInKitchen'))
        balcony = self.string_2_bool(self.get_element('resultlist.realEstate_balcony'))
        garden = self.string_2_bool(self.get_element('resultlist.realEstate_garden'))
        cellar = self.string_2_bool(self.get_element('obj_cellar'))
        lift = self.string_2_bool(self.get_element('obj_lift'))
        fully_accessible = self.string_2_bool(self.get_element('obj_barrierFree'))
        assisted_living = self.string_2_bool(self.get_element('obj_assistedLiving'))
        object_state = self.get_element('obj_condition')
        floor = self.get_element('obj_floor')
        firing_type = self.get_element('obj_firingTypes')
        heating_type = self.get_element('obj_heatingType')
        real_estate_type = self.get_element('obj_immotype')
        interior_quality = self.get_element('obj_interiorQual')
        flat_type = self.get_element('obj_typeOfFlat')
        year_construction = self.get_element('obj_yearConstructed')
        last_refurbish = self.get_element('obj_lastRefurbish')
        description = self.get_element('description')

        return pd.DataFrame({
            #  "date_start": [date_start],
            "expose_id": [expose_id],
            "street": [street],
            "street_hsno": [street_hsno],
            "postcode": [postcode],
            "city": [city],
            "title": [title],
            "private_offer": [private_offer],
            "rent_gross_eur": [rent_gross_eur],
            "rent_gross_marketing_type": [rent_gross_marketing_type],
            "rent_gross_interval_type": [rent_gross_interval_type],
            "rent_net_eur": [rent_net_eur],
            "rent_net_marketing_type": [rent_net_marketing_type],
            "rent_net_interval_type": [rent_net_interval_type],
            "rent_scope": [rent_scope],
            "living_space": [living_space_sqm],
            "sqm_price": sqm_price,
            "num_rooms": [num_rooms],
            "num_parking_spaces": [num_parking_spaces],
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
            "heating_type": [heating_type],
            "real_estate_type": [real_estate_type],
            "interior_quality": [interior_quality],
            "flat_type": [flat_type],
            "year_construction": [year_construction],
            "last_refurbish": [last_refurbish],
            "heating_costs": [heating_costs],
            "description": [description]})

    def get_element(self, key):
        """
            Searches in the "init_data" for a "key" and returns the value or a empty string
        :param key: str
            Searching "key"
        :return: value: any type
            Returns the found value and if the "key" does not exist, an empty string is returned
        """
        try:
            if isinstance(self.init_data.get(key), pd.Series) or isinstance(self.init_data.get(key), pd.DataFrame):
                return self.init_data[key].values[0]
            else:
                return self.init_data[key]

        except KeyError as e:
            print(key)
            print(e)
            # no element in data
            # return empty string
            return ''

    @staticmethod
    def string_2_bool(value):
        """
        Changes a string value into a boolean True or False based on a word list for strings that have the meaning of
        True
        :param value: str
        :return: boolean (True or False)
        """
        return value.lower() in ("y", "true")

    def set_type(self):
        """
        Sets the types for all columns of the data
        :return: None
        """
        try:
            self.data = self.data.astype(dtype={
                                    #  "date_start": "str",
                                    "expose_id": "int",
                                    "street": "str",
                                    "street_hsno": "str",
                                    "postcode": "str",  # Because it always has to have 5 digits
                                    "city": "str",
                                    "title": "str",
                                    "private_offer": "bool",
                                    "rent_gross_eur": "float",
                                    "rent_gross_marketing_type": "str",
                                    "rent_gross_interval_type": "str",
                                    "rent_net_eur": "float",
                                    "rent_net_marketing_type": "str",
                                    "rent_net_interval_type": "str",
                                    "rent_scope": "str",
                                    "living_space": "float",
                                    "sqm_price": "float",
                                    "num_rooms": "float",
                                    "num_parking_spaces": "str",
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
                                    "real_estate_type": "str",
                                    "interior_quality": "str",
                                    "flat_type": "str",
                                    "year_construction": "int",
                                    "last_refurbish": "int",
                                    "heating_costs": "float",
                                    "description": "str"
                                    }
            )
        except ValueError as e:
            print(e)

        except AttributeError as e:
            print(e)

    @property
    def get_data(self):
        """
        Getter, returns the data as a DataFrame
        :return: pandas.DataFrame
        """
        return self.data

    def get_address(self):
        """
        Return an address as a String (e.g. for geocoder) It´s composed of street and house number
        :return: str
        """
        return self.data["street"].values[0] + " " + self.data["street_hsno"].values[0]

    def set_coordinates(self, coordinates):
        """
        Gets coordinates as an input (e.g. from geocoder) and stores them in separate columns in the "data"
        :param coordinates: dict (accuracy, x, y)
        :return: None
        """
        self.data = self.data.assign(x=coordinates.get("x"))
        self.data = self.data.assign(y=coordinates.get("y"))
        self.data = self.data.assign(accuracy=coordinates.get("accuracy"))
