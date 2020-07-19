# -*- coding: utf-8 -*-
import scrapy


class PttItem(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    text = scrapy.Field()
    
