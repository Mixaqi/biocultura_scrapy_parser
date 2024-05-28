from __future__ import annotations

import scrapy


class SilbarcelonaItem(scrapy.Item):
    silbarcelona_link = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    address = scrapy.Field()

