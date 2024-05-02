from __future__ import annotations

import scrapy
from scrapy.item import Field


class Messefrankfurt1Item(scrapy.Item):
    name: str = Field(default="")
    street: str = Field(default="")
    city: str = Field(default="")
    zip_code: str = Field(default="")
    country: str = Field(default="")
    tel: str = Field(default="")
    fax: str = Field(default="")
    email: str = Field(default="")
    whatsapp_link = Field(default="")