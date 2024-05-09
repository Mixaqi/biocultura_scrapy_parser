from __future__ import annotations

import scrapy


class Exhibitor2Item(scrapy.Item):
    link = scrapy.Field()
    email = scrapy.Field()
    address = scrapy.Field()
    title = scrapy.Field()
