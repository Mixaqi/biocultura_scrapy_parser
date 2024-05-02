from __future__ import annotations

BOT_NAME = "messefrankfurt1"

SPIDER_MODULES = ["messefrankfurt1.spiders"]
NEWSPIDER_MODULE = "messefrankfurt1.spiders"


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"


# Obey robots.txt rules
ROBOTSTXT_OBEY = True


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

