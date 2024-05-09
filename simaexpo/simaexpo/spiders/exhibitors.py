from __future__ import annotations

import scrapy


class ExhibitorsSpider(scrapy.Spider):
    name = "exhibitors"
    allowed_domains = ["simaexpo.com"]
    start_urls = ["https://simaexpo.com/expositores/"]

    def parse(self, response):
        links = response.css("div.ficha-data h2 a::attr(href)").extract()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_exhibitor)

    def parse_exhibitor(self, response):
        title = response.css("h1::text").get()
        links = response.css("div.single-bloque-social a.fs1.global.fa-solid.fa-globe::attr(href)").extract()
        whatsapp = response.css("div.single-bloque-social a.fs1.whatsapp.fa-brands.fa-square-whatsapp::attr(href)").extract()
        email = response.css("div.single-bloque-content-main p:last-of-type a::attr(title)").get()
        address = response.xpath("//div[contains(@class, 'single-bloque-content-main')]/p[span[position() >= 4]]/text()").get()
        yield {
            "title": title,
            "link": links,
            "whatsapp": whatsapp,
            "email": email,
            "address": address,
        }
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_detail)

    def parse_detail(self, response):
        title = response.css("h1::text").get()
        yield {
            "title": title,
            "link": response.url,
        }
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_detail)
