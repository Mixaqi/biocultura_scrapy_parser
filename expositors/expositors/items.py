from __future__ import annotations

from scrapy.item import Field


class ExpositorsItem(scrapy.Item):
    title = Field()
    link = Field()
    contact_name = Field()
    email = Field()
    phone = Field()
    country = Field()


