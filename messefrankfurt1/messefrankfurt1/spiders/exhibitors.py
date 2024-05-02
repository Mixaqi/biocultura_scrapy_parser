from __future__ import annotations

from typing import Generator

import scrapy
from scrapy import Request

from ..items import Messefrankfurt1Item


class ExhibitorsSpider(scrapy.Spider):
    name = "exhibitors"
    start_urls: Generator[str, None, None] = (
        f"https://api.messefrankfurt.com/service/esb_api/exhibitor-service/api/2.1/public/exhibitor/search?language=en-GB&q=&orderBy=name&pageNumber={i}&pageSize=25&showJumpLabels=true&findEventVariable=TEXWORLDPARISSPRING"
        for i in range(1, 101)
    )
    api_key = "LXnMWcYQhipLAS7rImEzmZ3CkrU033FMha9cwVSngG4vbufTsAOCQQ=="

    def start_requests(self) -> Generator[Request, None, None]:
        for url in self.start_urls:
            headers = {"Apikey": self.api_key}
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response) -> Generator[Messefrankfurt1Item, None, None]:
        data = response.json()
        hits = data.get("result", {}).get("hits", [])

        for hit in hits:
            exhibitor = hit.get("exhibitor", {})
            item = Messefrankfurt1Item()
            item["name"] = exhibitor.get("name")
            address = exhibitor.get("address", {})
            item["street"] = address.get("street")
            item["city"] = address.get("city")
            item["zip_code"] = address.get("zip")
            item["country"] = address.get("country", {}).get("label")
            item["tel"] = address.get("tel")
            item["fax"] = address.get("fax")
            item["email"] = address.get("email")

            yield item
