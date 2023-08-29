# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    date = scrapy.Field()


class NewsWebsiteCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
