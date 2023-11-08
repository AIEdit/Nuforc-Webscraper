# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NurfocItem(scrapy.Item):
    link:str = scrapy.Field()
    occured:str = scrapy.Field()
    city:str = scrapy.Field()
    state:str = scrapy.Field()
    country:str = scrapy.Field()
    shape:str = scrapy.Field()
    summary:str = scrapy.Field()
    reported:str = scrapy.Field()
    posted:str = scrapy.Field()
    image:str = scrapy.Field()
    sighting_id:str = scrapy.Field()
    notes:str = scrapy.Field()

