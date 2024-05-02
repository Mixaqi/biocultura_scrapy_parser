from __future__ import annotations

import scrapy


class SponsorSpider(scrapy.Spider):
    name = "eccmid"
    start_urls = ["https://www.eccmid.org/sponsorship-and-exhibition/sponsor-list"]

    def parse(self, response):
        sponsor_links = response.xpath("//a[@class='linksside']")
        for sponsor_link in sponsor_links:
            title = sponsor_link.xpath("text()").get()
            link = sponsor_link.xpath("@href").get()
            yield response.follow(link, callback=self.parse_sponsor_page, meta={"title": title})

    def parse_sponsor_page(self, response):
        title = response.meta["title"]
        html_content = response.body

        yield {
            "title": title,
            "html_content": html_content,
        }

