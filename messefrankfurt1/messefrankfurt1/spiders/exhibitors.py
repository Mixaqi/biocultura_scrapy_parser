from __future__ import annotations

import html
from typing import Generator

import scrapy
from dotenv import load_dotenv

from ..items import Messefrankfurt1Item
from ..whatsapp_service import WhatsappService
from .exhibitor2 import clean_phone_number

load_dotenv()

class ExhibitorsSpider(scrapy.Spider):
    name = "exhibitors"
    start_urls: Generator[str, None, None] = (
        f"https://api.messefrankfurt.com/service/esb_api/exhibitor-service/api/2.1/public/exhibitor/search?language=en-GB&q=&orderBy=name&pageNumber={i}&pageSize=25&showJumpLabels=true&findEventVariable=TEXWORLDPARISSPRING"
        for i in range(1, 101)
    )
    api_key = "LXnMWcYQhipLAS7rImEzmZ3CkrU033FMha9cwVSngG4vbufTsAOCQQ=="

    def start_requests(self):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Content-Type": "text/html; charset=utf-8",
        }
        for url in self.start_urls:
            headers = {"Apikey": self.api_key}
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    async def parse(self, response):
        data = response.json()
        hits = data.get("result", {}).get("hits", [])

        whatsapp_service = WhatsappService(7103909222, "0b7c68fbd0284e098b454ef95d925bf43c48b75d0cc14415a7")

        for hit in hits:
            exhibitor = hit.get("exhibitor", {})
            item = Messefrankfurt1Item()
            item["name"] = html.unescape(exhibitor.get("name", ""))  # Декодирование HTML-сущностей

            address = exhibitor.get("address", {})
            item["city"] = address.get("city")
            item["zip_code"] = address.get("zip")
            item["country"] = address.get("country", {}).get("label")
            item["tel"] = clean_phone_number(address.get("tel"))
            item["fax"] = clean_phone_number(address.get("fax"))
            item["email"] = address.get("email")

            self.logger.info(f"Processing item {item['name']}")
            self.logger.info(f"Cleaned phone number: {item['tel']}")

            whatsapp_link = await whatsapp_service.format_to_whatsapp_link(item["tel"])

            if whatsapp_link:
                self.logger.info(f"WhatsApp link: {whatsapp_link}")
            else:
                self.logger.info("No WhatsApp link found")

            item["whatsapp_link"] = whatsapp_link

            yield item
