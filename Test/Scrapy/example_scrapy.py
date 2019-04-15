# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.crawler import CrawlerProcess
from Test.Scrapy.items import ImmoscoutItem


class ImmoscoutScrapyExample(scrapy.Spider):
    name = "immoscout"
    allowed_domains = ["immobilienscout24.de"]
    url = 'https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/-/2,50-/60,00-/EURO--1000,00'
    # url = 'https://www.immowelt.de/liste/essen/wohnungen/mieten?prima=400&wflmi=40&roomi=3&sort=relevanz'
    script_xpath = './/script[contains(., "IS24.resultList")]'
    next_xpath = '//div[@id = "pager"]/div/a/@href'

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        i = 1
        print('response.url', response.url)

        lines = response.xpath(self.script_xpath).extract_first().split('\n')
        for line in lines:
            if line.strip().startswith('resultListModel'):
                print('I = ', i)
                i += 1
                immo_json = line.strip()
                print(immo_json)
                immo_json = json.loads(immo_json[17:-1])

                immo_entries = immo_json["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0][
                    "resultlistEntry"]

                for result in immo_entries:

                    item = ImmoscoutItem()

                    data = result["resultlist.realEstate"]

                    item['immo_id'] = data['@id']
                    item['url'] = response.urljoin("/expose/" + str(data['@id']))
                    item['title'] = data['title']
                    address = data['address']
                    try:
                        item['address'] = address['street'] + " " + address['houseNumber']
                    except:
                        item['address'] = None
                    item['city'] = address['city']
                    item['zip_code'] = address['postcode']
                    item['district'] = address['quarter']

                    item["rent"] = data["price"]["value"]
                    item["sqm"] = data["livingSpace"]
                    item["rooms"] = data["numberOfRooms"]

                    if "calculatedPrice" in data:
                        item["extra_costs"] = (data["calculatedPrice"]["value"] - data["price"]["value"])
                    if "builtInKitchen" in data:
                        item["kitchen"] = data["builtInKitchen"]
                    if "balcony" in data:
                        item["balcony"] = data["balcony"]
                    if "garden" in data:
                        item["garden"] = data["garden"]
                    if "privateOffer" in data:
                        item["private"] = data["privateOffer"]
                    if "plotArea" in data:
                        item["area"] = data["plotArea"]
                    if "cellar" in data:
                        item["cellar"] = data["cellar"]

                    try:
                        contact = data['contactDetails']
                        item['contact_name'] = contact['firstname'] + " " + contact["lastname"]
                    except:
                        item['contact_name'] = None

                    try:
                        item['media_count'] = len(data['galleryAttachments']['attachment'])
                    except:
                        item['media_count'] = 0

                    try:
                        item['lat'] = address['wgs84Coordinate']['latitude']
                        item['lng'] = address['wgs84Coordinate']['longitude']
                    except:
                        item['lat'] = None
                        item['lng'] = None

                    yield item

        next_page_list = response.xpath(self.next_xpath).extract()
        if next_page_list:
            next_page = next_page_list[-1]
            print("Scraping next page", next_page)
            if next_page:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(ImmoscoutScrapyExample)
# the script will block here until the crawling is finished
process.start()
