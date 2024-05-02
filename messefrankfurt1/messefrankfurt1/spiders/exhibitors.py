from __future__ import annotations

from typing import Generator, Optional

import scrapy
from dotenv import load_dotenv
from scrapy import Request

from ..items import Messefrankfurt1Item
from ..whatsapp_service import WhatsappService

load_dotenv()

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

    async def parse(self, response) -> Generator[Messefrankfurt1Item, None, None]:
        data = response.json()
        hits = data.get("result", {}).get("hits", [])

        whatsapp_service = WhatsappService(7103909222, "0b7c68fbd0284e098b454ef95d925bf43c48b75d0cc14415a7")

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

            # Обработка номера телефона перед вызовом метода format_to_whatsapp_link
            phone_number = address.get("tel")
            if phone_number:
                phone_number = phone_number.replace(" ", "")
                if phone_number.startswith("+"):
                    phone_number = phone_number[1:]

            # Логирование значений перед отправкой запроса
            self.logger.info(f"Processing item {item['name']}")
            self.logger.info(f"Phone number: {phone_number}")

            whatsapp_link: Optional[str] = await whatsapp_service.format_to_whatsapp_link(phone_number)

            # Логирование результата запроса
            if whatsapp_link:
                self.logger.info(f"WhatsApp link: {whatsapp_link}")
            else:
                self.logger.info("No WhatsApp link found")

            item["whatsapp_link"] = whatsapp_link

            yield item
