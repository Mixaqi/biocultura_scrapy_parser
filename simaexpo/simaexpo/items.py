from __future__ import annotations

import scrapy


class Exhibitor2Item(scrapy.Item):
    link = scrapy.Field()
    email = scrapy.Field()
    address = scrapy.Field()
    title = scrapy.Field()

class ExhibitorItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    whatsapp = scrapy.Field()
    email = scrapy.Field()
    address = scrapy.Field()
    # html_content = scrapy.Field()
    phone_number = scrapy.Field()
