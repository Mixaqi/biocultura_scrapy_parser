from __future__ import annotations

import re

import scrapy
from bs4 import BeautifulSoup

from ..items import Exhibitor2Item


class ExhibitorsSpider(scrapy.Spider):
    name = "exhibitors2"
    start_urls = ["https://simaexpo.com/expositores/"]

    def parse(self, response):
        for link in response.css("div.ficha-data h2 a::attr(href)"):
            yield response.follow(link, callback=self.parse_exhibitor)

    def parse_exhibitor(self, response):
        item = Exhibitor2Item()
        exhibitor_link = response.css("div.single-bloque-social a.fs1.global.fa-solid.fa-globe::attr(href)").extract_first()
        item["title"] = response.css("h1::text").get()
        item["link"] = exhibitor_link if exhibitor_link else ""
        item["email"] = response.css("div.single-bloque-content-main p:last-of-type a::attr(title)").get() or ""
        address = response.xpath("//div[contains(@class, 'single-bloque-content-main')]/p[span[position() >= 4]]/text()").get()
        item["address"] = address if address else ""
        yield item

        if exhibitor_link:
            yield response.follow(exhibitor_link, callback=self.parse_exhibitor_link, meta={"item": item})

    def parse_exhibitor_link(self, response):
        item = response.meta["item"]
        soup = BeautifulSoup(response.body, "lxml")
        html_text = soup.get_text().replace("\n", "").replace("\t", "").strip()
        phone_pattern = re.compile(r"\+?\d{1,3}\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}")
        phone_numbers = phone_pattern.findall(html_text)
        item["phone_number"] = phone_numbers
        yield item
