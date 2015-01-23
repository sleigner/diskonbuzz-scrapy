# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join


class PromopediaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    promo_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    start_date = scrapy.Field()
    expiry_date = scrapy.Field()
    issuer = scrapy.Field()
    store = scrapy.Field()

class PromopediaLoader(ItemLoader):
    default_output_processor = TakeFirst()
