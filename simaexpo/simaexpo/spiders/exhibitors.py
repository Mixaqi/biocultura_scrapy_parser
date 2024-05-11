from __future__ import annotations

import scrapy

from ..items import ExhibitorItem


class ExhibitorsSpider(scrapy.Spider):
    name = "exhibitors"
    start_urls = ["https://simaexpo.com/expositores/"]

    def parse(self, response):
        links = response.css("div.ficha-data h2 a::attr(href)").extract()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_exhibitor)

    def parse_exhibitor(self, response):
        item = ExhibitorItem()
        item["title"] = response.css("h1::text").get()
        item["link"] = response.css("div.single-bloque-social a.fs1.global.fa-solid.fa-globe::attr(href)").extract()
        item["whatsapp"] = response.css("div.single-bloque-social a.fs1.whatsapp.fa-brands.fa-square-whatsapp::attr(href)").extract()
        item["email"] = response.css("div.single-bloque-content-main p:last-of-type a::attr(title)").get()
        item["address"] = response.xpath("//div[contains(@class, 'single-bloque-content-main')]/p[span[position() >= 4]]/text()").get()

    #     # Выкачиваем HTML из каждой ссылки
    #     for link in item["link"]:
    #         yield scrapy.Request(url=link, callback=self.parse_html, meta={"item": item})

    # def parse_html(self, response):
    #     item = response.meta["item"]
    #     # Извлекаем номер телефона с помощью регулярного выражения
    #     phone_pattern = re.compile(r"([+]\w{13,20})")
    #     phone_numbers = re.findall(phone_pattern, response.text)
    #     phone_number = phone_numbers[0] if phone_numbers else None  # Берем первый найденный номер
    #     item["phone_number"] = phone_number

