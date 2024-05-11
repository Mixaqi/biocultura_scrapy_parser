from __future__ import annotations

import scrapy

from ..items import Exhibitor2Item


class ExhibitorsSpider(scrapy.Spider):
    name = "exhibitors2"
    start_urls = ["https://simaexpo.com/expositores/"]

    def parse(self, response):
        for link in response.css("div.ficha-data h2 a::attr(href)"):
            yield response.follow(link, callback=self.parse_exhibitor)

    # def parse_exhibitor(self, response):
    #     exhibitor_link = response.css("div.single-bloque-social a.fs1.global.fa-solid.fa-globe::attr(href)").extract_first()
    #     yield {
    #         "title": response.css("title::text").get(),
    #         "link": exhibitor_link,
    #         "email": response.css("div.single-bloque-content-main p:last-of-type a::attr(title)").get(),
    #         "address": response.xpath("//div[contains(@class, 'single-bloque-content-main')]/p[span[position() >= 4]]/text()").get(),
    #     }
    #     if exhibitor_link:
    #         # yield response.follow(exhibitor_link, callback=self.parse_exhibitor_link)
    #         yield scrapy.Request(url=exhibitor_link, callback=self.parse_exhibitor_link)

    def parse_exhibitor(self, response):
        item = Exhibitor2Item()
        exhibitor_link = response.css("div.single-bloque-social a.fs1.global.fa-solid.fa-globe::attr(href)").extract_first()
        item["title"] = response.css("h1::text").get()
        item["link"] = exhibitor_link if exhibitor_link else ""
        item["email"] = response.css("div.single-bloque-content-main p:last-of-type a::attr(title)").get() or ""
        address = response.xpath("//div[contains(@class, 'single-bloque-content-main')]/p[span[position() >= 4]]/text()").get()
        item["address"] = address if address else ""
        yield item

        
    def parse_exhibitor_link(self, response):
        title = response.css("title::text").get()
        yield {
            "title": title,
        }
