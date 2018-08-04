# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WarehouseParserItem(scrapy.Item):
    title = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    currency = scrapy.Field()
    size = scrapy.Field()
    image = scrapy.Field()
