"""
Description:  Data model for uniform storage of the scraped data of Immobilienscout24 webpage
Author: Marlena Hecker, marlena.hecker@hs-bochum.de
"""

import pandas as pd


class ImmoDataModel:

    def __init__(self, data):
        self.init_data = data
        self.data = self.prepare_data()

    def prepare_data(self):
        """
        Extracts relevant data from the input data
        It returns a pandas.DataFrame, which contains the unified data of the scraper
        :param: data as pandas.DataFrame or Dict
        :return: pandas DataFrame
        """
        # meta information
        expose_id = self.get_element('@id')
        title = self.get_element('resultlist.realEstate_title').replace("\n", "").replace("\/", "/")

        # real estate provider
        private_offer = self.string_2_bool(self.get_element('resultlist.realEstate_privateOffer'))
        customer_id = self.get_element('resultlist.realEstate_companyWideCustomerId')
        company = self.get_element('resultlist.realEstate_contactDetails_company')

        # new construction
        new_home_builder = self.string_2_bool(self.get_element('newHomeBuilder'))
        new_flag = self.get_element('hasNewFlag')
        newly_const = self.get_element('obj_newlyConst')

        # real estate type
        search_type = self.get_element('resultlist.realEstate_@xsi.type')
        type_of_flat = self.get_element('obj_typeOfFlat')
        immo_type = self.get_element('obj_immotype')
        exclusive_expose = self.get_element('obj_ExclusiveExpose')

        # dates entry
        creation_date = self.get_element('@creation')
        modification_date = self.get_element('@modification')
        publish_date = self.get_element('@publishDate')
        extraction_date = self.get_element('extraction_date')

        # pictures
        picture_creation_date = self.get_element('resultlist.realEstate_titlePicture_@creation')
        picture_modification_date = self.get_element('resultlist.realEstate_titlePicture_@modification')
        picture_publish_date = self.get_element('resultlist.realEstate_titlePicture_@publishDate')

        title_picture = self.string_2_bool(self.get_element('resultlist.realEstate_titlePicture_titlePicture'))
        number_pictures = self.get_element('obj_picturecount')
        picture_trend = self.get_element('obj_pricetrend')

        # address
        street = self.get_element('resultlist.realEstate_address_street')
        street_house_number = self.get_element('resultlist.realEstate_address_houseNumber')

        street_house_number, house_number_supplement = self.house_number(street_house_number)

        postcode = self.get_element('resultlist.realEstate_address_postcode')
        quarter = self.get_element('resultlist.realEstate_address_quarter')
        city = self.get_element('resultlist.realEstate_address_city')
        region = self.get_element('obj_regio1')
        country = self.get_element('geo_land')
        full_address = self.get_element('resultlist.realEstate_address_description_text')

        # coordinates
        latitude = self.get_element('resultlist.realEstate_address_wgs84Coordinate_latitude')
        longitude = self.get_element('resultlist.realEstate_address_wgs84Coordinate_longitude')
        precise_house_number = self.string_2_bool(self.get_element('resultlist.realEstate_address_preciseHouseNumber'))

        # rent
        rent_gross_eur = self.get_element('resultlist.realEstate_calculatedPrice_value')
        rent_net_eur = self.get_element('resultlist.realEstate_price_value')
        service_charge = self.get_element('obj_serviceCharge')
        total_rent = self.get_element('obj_totalRent')
        price_currency = self.get_element('resultlist.realEstate_price_currency')

        price_trend_buy = self.get_element('obj_pricetrendbuy')
        price_trend_rent = self.get_element('obj_pricetrendrent')
        base_rent_range = self.get_element('obj_baseRentRange')

        rent_scope = self.get_element('resultlist.realEstate_calculatedPrice_rentScope')

        rent_gross_marketing_type = self.get_element('resultlist.realEstate_price_marketingType')
        rent_net_marketing_type = self.get_element('resultlist.realEstate_calculatedPrice_marketingType')

        rent_gross_interval_type = self.get_element('resultlist.realEstate_price_priceIntervalType')
        rent_net_interval_type = self.get_element('resultlist.realEstate_calculatedPrice_priceIntervalType')

        # characteristics of a real estate
        living_space_sqm = self.get_element('resultlist.realEstate_livingSpace')
        sqm_price = float(rent_gross_eur) / float(living_space_sqm)

        num_rooms = self.get_element('resultlist.realEstate_numberOfRooms')
        no_rooms_range = self.get_element('obj_noRoomsRange')

        floor = self.get_element('obj_floor')
        number_of_floors = self.get_element('obj_numberOfFloors')

        fully_accessible = self.string_2_bool(self.get_element('obj_barrierFree'))
        assisted_living = self.string_2_bool(self.get_element('obj_assistedLiving'))
        object_state = self.get_element('obj_condition')
        pets_allowed = self.pets_allowed(self.get_element('obj_petsAllowed'))
        interior_quality = self.get_element('obj_interiorQual')

        num_parking_spaces = self.get_element("obj_noParkSpaces")

        builtin_kitchen = self.string_2_bool(self.get_element('resultlist.realEstate_builtInKitchen'))
        balcony = self.string_2_bool(self.get_element('resultlist.realEstate_balcony'))
        garden = self.string_2_bool(self.get_element('resultlist.realEstate_garden'))
        cellar = self.string_2_bool(self.get_element('obj_cellar'))
        lift = self.string_2_bool(self.get_element('obj_lift'))
        shared_flat_suitable = self.shared_flat_suitable(self.get_element('realEstateTags_tag'))

        tags = self.get_element('realEstateTags_tag')
        if isinstance(tags, list):
            tags = ', '.join(tags)

        # energy
        heating_type = self.get_element('obj_heatingType')

        heating_costs = self.get_element('obj_heatingCosts')
        firing_type = self.get_element('obj_firingTypes')

        energy_type = self.get_element('obj_energyType')
        energy_efficiency_class = self.get_element('obj_energyEfficiencyClass')
        termal_char = self.get_element('obj_thermalChar')

        # construction
        year_construction = self.get_element('obj_yearConstructed')
        year_constructed_range = self.get_element('obj_yearConstructedRange')
        last_refurbish = self.get_element('obj_lastRefurbish')

        description = self.get_element('description')

        # internet
        internet_type = self.get_element('obj_telekomInternetType')
        internet_upload_speed = self.get_element('obj_telekomUploadSpeed')
        internet_download_speed = self.get_element('obj_telekomDownloadSpeed')
        internet_technology = self.get_element('obj_telekomInternetTechnology')

        # Offer of living space, offer of rentable and buyable living space on the housing market
        living_space_range = self.get_element('obj_livingSpaceRange')

        return pd.DataFrame({
            "expose_id": [expose_id],

            "title": [title],

            "creation_date": [creation_date],
            "modification_date": [modification_date],
            "publish_date": [publish_date],
            "extraction_date": [extraction_date],
            "remove_date": [""],
            "duration": [""],

            "picture_creation_date": [picture_creation_date],
            "picture_modification_date": [picture_modification_date],
            "picture_publish_date": [picture_publish_date],
            "title_picture": [title_picture],
            "number_pictures": [number_pictures],
            "picture_trend": [picture_trend],

            "street": [street],
            "street_house_number": [street_house_number],
            "house_number_supplement": [house_number_supplement],
            "quarter": [quarter],
            "postcode": [postcode],
            "city": [city],
            "region": [region],
            "country": [country],
            "full_address": [full_address],

            "latitude": [latitude],
            "longitude": [longitude],
            "precise_house_number": [precise_house_number],
            "X": [0],
            "Y": [0],
            "accuracy": [0],
            "source": [""],

            "private_offer": [private_offer],
            "customer_id": [customer_id],
            "company": [company],

            "new_home_builder": [new_home_builder],
            "new_falg": [new_flag],
            "newly_const": [newly_const],

            "search_type": [search_type],
            "type_of_flat": [type_of_flat],
            "immo_type": [immo_type],
            "exclusive_expose": [exclusive_expose],


            "rent_gross_eur": [rent_gross_eur],
            "rent_net_eur": [rent_net_eur],
            "service_charge": [service_charge],
            "total_rent": [total_rent],
            "price_currency": [price_currency],
            "rent_gross_marketing_type": [rent_gross_marketing_type],
            "rent_gross_interval_type": [rent_gross_interval_type],
            "rent_net_marketing_type": [rent_net_marketing_type],
            "rent_net_interval_type": [rent_net_interval_type],

            "price_trend_buy": [price_trend_buy],
            "price_trend_rent": [price_trend_rent],
            "base_rent_range": [base_rent_range],

            "rent_scope": [rent_scope],

            "living_space": [living_space_sqm],
            "sqm_price": [sqm_price],
            "living_space_range": [living_space_range],
            "num_rooms": [num_rooms],
            "no_rooms_range": [no_rooms_range],

            "interior_quality": [interior_quality],
            "year_construction": [year_construction],
            "year_constructed_range": [year_constructed_range],
            "last_refurbish": [last_refurbish],

            "num_parking_spaces": [num_parking_spaces],
            "builtin_kitchen": [builtin_kitchen],
            "balcony": [balcony],
            "garden": [garden],
            "cellar": [cellar],
            "lift": [lift],
            "fully_accessible": [fully_accessible],
            "assisted_living": [assisted_living],

            "object_state": [object_state],
            "floor": [floor],
            "number_of_floors": [number_of_floors],
            "pets_allowed": [pets_allowed],
            "shared_flat_suitable": [shared_flat_suitable],

            "heating_type": [heating_type],
            "firing_type": [firing_type],
            "energy_type": [energy_type],
            "energy_efficiency_class": [energy_efficiency_class],
            "termal_char": [termal_char],
            "heating_costs": [heating_costs],

            "internet_type": [internet_type],
            "internet_upload_speed": [internet_upload_speed],
            "internet_download_speed": [internet_download_speed],
            "internet_technology": [internet_technology],

            "tags": [tags],
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
            # print('Element not found: ', e)
            # no element in data and return empty string
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

    @staticmethod
    def house_number(house_number):
        head = house_number.rstrip('0123456789')
        tail = house_number[len(head):]
        return head, tail

    @staticmethod
    def shared_flat_suitable(attr):
        return "WG-geeignet" in attr

    def pets_allowed(self, attr):
        if attr in ("y", "true"):
            return self.string_2_bool(attr)
        else:
            return attr

    @property
    def get_data(self):
        """
        Getter, returns the data as a DataFrame
        :return: pandas.DataFrame
        """
        return self.data

    def get_value(self, value):
        """
        Return an address as a String (e.g. for geocoder) It´s composed of street and house number
        :return: str
        """
        return self.data[value].values[0]

    def get_address(self):
        return {"street": self.data['street'].values[0],
                "street_house_number": self.data['street_house_number'].values[0],
                "house_number_supplement": self.data['house_number_supplement'].values[0],
                "city": self.data['city'].values[0]}

    def check_coordinates(self):
        return self.data['X'].values[0] != 0 & self.data['Y'].values[0] != 0

    def set_coordinates(self, coordinates):
        """
        Gets coordinates as an input (e.g. from geocoder) and stores them in separate columns in the "data"
        :param coordinates: dict (accuracy, x, y)
        :return: None
        """
        self.data.at[0, 'X'] = coordinates['x']
        self.data.at[0, 'Y'] = coordinates['y']
        self.data.at[0, 'accuracy'] = coordinates['accuracy']
        self.data.at[0, 'source'] = coordinates['source']

        # self.data = self.data.assign(x=coordinates.get("x"))
        # self.data = self.data.assign(y=coordinates.get("y"))
        # self.data = self.data.assign(accuracy=coordinates.get("accuracy"))
