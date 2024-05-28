from __future__ import annotations

import scrapy

from silbarcelona.items import SilbarcelonaItem


class ExhibitorsSpider(scrapy.Spider):
    name = "exhibitors"
    start_urls = ["https://www.silbcn.com/es/informacion/empresas_participantes.html"]

    def parse(self, response):
        for link in response.css("a.btnxe::attr(href)")[1:]:
            sibarcelona_link = response.urljoin(link.get())
            yield response.follow(link, callback=self.parse_exhibitor, meta={"silbarcelona_link": sibarcelona_link})

    def parse_exhibitor(self, response):
        item = SilbarcelonaItem()
        item["silbarcelona_link"] = response.meta.get("silbarcelona_link")
        item["title"] = response.css("div[style='background-color:#f0f0f0; padding:5px; color:#000; font-size: 24px; font-weight: bold;']::text").get().strip()
        item["link"] = response.css("a[style='font-family:Arial, Helvetica, sans-serif; font-size:14px; color:#ff8196; text-decoration:none;']::text").get().strip()
        phone = response.xpath("//td[@valign='top' and @align='left']/text()").get().strip()
        item["phone"] = clean_phone_number(phone)

        address_parts = response.xpath("//td[@valign='top' and @align='left']/br/following-sibling::text()").getall()
        if len(address_parts) > 1:
            item["address"] = address_parts[1].strip()
        else:
            item["address"] = None
            
        yield item


def clean_phone_number(phone_number: str) -> str:
    cleaned_number = "".join(ch for ch in phone_number if ch.isdigit())
    return cleaned_number
