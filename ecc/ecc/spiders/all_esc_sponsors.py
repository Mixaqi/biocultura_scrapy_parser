from __future__ import annotations

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SponsorSpider(CrawlSpider):
    name = "all_esc_sponsors"
    start_urls = ["https://www.eccmid.org/sponsorship-and-exhibition/sponsor-list"]

    rules = (
        Rule(LinkExtractor(allow="sponsorship-and-exhibition/sponsor-list",
                           restrict_xpaths="//a[@class='linksside']/@href")),
    )

    def parse_sponsor_list(self, response):
        links = response.xpath("//a[@class='linksside']/@href").getall()
        print(links)

# response.xpath("//a[@class='linksside']/@href").getall()