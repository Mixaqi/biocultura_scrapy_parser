from __future__ import annotations

from typing import Generator

import scrapy


class ExpositorSpider(scrapy.Spider):
    name = "expositor_spider"
    allowed_domains = ["biocultura.org"]
    # base_url = "https://www.biocultura.org/expositor/"

    def start_requests(self)-> Generator[scrapy.Request, None, None]:
        base_url = "https://www.biocultura.org/expositor/"
        for i in range(150000, 150600):
            url = f"{base_url}{i}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.Response) -> Generator[dict[str, str], None, None]:
        title: str = response.css("h2.heading-2.expositor-title::text").get()
        link: str = response.css("a.red-button::text").get()
        contact_name: str = response.css("div.expositor-contact p::text")[0].get()
        email: str = response.css("div.expositor-contact p::text")[1].get()
        phone: str = "".join(response.xpath("//div[@class='expositor-contact']/text()").re(r"\S+"))
        country: str = response.css("div.expositor-contact p::text")[-1].get()

        yield {"title": title,
                "link": link,
                "contact_name": contact_name,
                "email": email,
                "phone": phone,
                "country": country,
        }
