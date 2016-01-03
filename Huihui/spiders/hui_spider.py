# -*- coding: utf-8 -*-
__author__ = 'dearx'

from scrapy import Spider
from scrapy.selector import Selector

#数据模型
from Huihui.items import HuihuiItem

class HuiSpider(Spider):
    #实例化属性
    name = "huihui"
    allowed_domains = ["http://www.huihui.cn"]
    start_urls = [
        "http://www.huihui.cn/all?page=1",
    ]

    #爬虫方法
    def parse(self, response):
        #促销
        sales = Selector(response).xpath('//li[@class="hui-list-item1"]')
        #print sales.extract()

        # for sale in sales:
        #     #声明模型
        #     item = HuihuiItem()
        #
        #     item['title'] = sale.xpath('//h3/a/text()').extract()
        #     item['imageURL'] = sale.xpath('//div[@class="hlist-list-pic"]/a/img/@data-src').extract()
        #     item['detail'] = sale.xpath('//div[@class="hui-content-text"]/p/text()').extract()
        #     item['itemURL'] = sale.xpath('//h3/a/@href').extract()
        #     item['itemfrom'] = sale.xpath('//div[@class="list-shop"]/a/text()').extract()
        #     item['hot'] = sale.xpath('//h3/a/em/text()').extract()
        #
        #     yield item

        titles = sales.xpath('//h3/a/text()').extract()
        imageURLs = sales.xpath('//div[@class="hlist-list-pic"]/a/img/@data-src').extract()
        details = sales.xpath('//div[@class="hui-content-text"]/p/text()').extract()
        itemURLs = sales.xpath('//h3/a/@href').extract()
        itemfroms = sales.xpath('//div[@class="list-shop"]/a/text()').extract()
        hots = sales.xpath('//h3/a/em/text()').extract()

        for index in range(len(sales)):
            print "创建数据模型"
            item = HuihuiItem()

            item["title"] = titles[index]
            item["imageURL"] = imageURLs[index]
            item["detail"] = details[index]
            item["itemURL"] = itemURLs[index]
            item["itemfrom"] = itemfroms[index]
            item["hot"] = hots[index]

            yield item

        print '数据转模型完毕'

