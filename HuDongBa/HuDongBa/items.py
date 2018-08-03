# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HudongbaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    imageUrl = scrapy.Field()
    startDate = scrapy.Field()
    endDate = scrapy.Field()
    address = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()

    pass
