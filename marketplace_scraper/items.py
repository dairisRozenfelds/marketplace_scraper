# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SsCarsItemDeep(scrapy.Item):
    group = scrapy.Field()
    name = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    engine = scrapy.Field()
    gearbox = scrapy.Field()
    mileage = scrapy.Field()
    color = scrapy.Field()
    TA = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    date_added = scrapy.Field()
    pass

class SsCarsItem(scrapy.Item):
    group = scrapy.Field()
    name = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    engine = scrapy.Field()
    mileage = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    pass

class AutopliusCarsItem(scrapy.Item):
    group = scrapy.Field()
    name = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    engine = scrapy.Field()
    mileage = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    pass