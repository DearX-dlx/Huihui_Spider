# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item,Field

class HuihuiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #标题
    title = Field()
    #图片
    imageURL = Field()
    #描叙
    detail = Field()
    #URL
    itemURL = Field()
    #来源
    itemfrom = Field()
    #热点
    hot = Field()

    pass
