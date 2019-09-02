#!/usr/bin/python
import scrapy
from html.parser import HTMLParser

# Criacao do objeto Spider
class Crawler(scrapy.Spider):
    name = 'items'
    start_urls = [
        'https://revistaautoesporte.globo.com/rss/ultimas/feed.xml',
    ]

    # Separacao dos objetos por tipo de dado
    def parse(self, response):
        h = HTMLParser()
        for item in response.css('item'):
            yield {
                'title': item.css('title::text').get(),
                'link': item.css('link::text').get(),
                'description': h.unescape(item.css('description::text').get()),
            }

