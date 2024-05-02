from __future__ import annotations

import json

import scrapy
from scrapy import Request


class ExhibitorsSpider(scrapy.Spider):
    name = "exhibitors"
    start_urls = [
        "https://api.messefrankfurt.com/service/esb_api/exhibitor-service/api/2.1/public/exhibitor/search?language=en-GB&q=&orderBy=name&pageNumber=%d&pageSize=25&showJumpLabels=true&findEventVariable=TEXWORLDPARISSPRING" % i
        for i in range(1, 101)
    ]
    api_key = "LXnMWcYQhipLAS7rImEzmZ3CkrU033FMha9cwVSngG4vbufTsAOCQQ=="

    def start_requests(self):
        for url in self.start_urls:
            headers = {"Apikey": self.api_key}
            yield Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        hits = data.get("result", {}).get("hits", [])

        for hit in hits:
            exhibitor = hit.get("exhibitor", {})
            name = exhibitor.get("name")
            address = exhibitor.get("address", {})
            street = address.get("street")
            city = address.get("city")
            zip_code = address.get("zip")
            country = address.get("country", {}).get("label")

            yield {
                "name": name,
                "address": {
                    "street": street,
                    "city": city,
                    "zip": zip_code,
                    "country": country,
                },
            }
