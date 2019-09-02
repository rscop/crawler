#!/usr/bin/python
import scrapy

# Criacao do objeto Spider
class Crawler(scrapy.Spider):
    name = 'items'
    start_urls = [
        'https://revistaautoesporte.globo.com/rss/ultimas/feed.xml',
    ]

    # Separacao dos objetos por tipo de dado
    def parse(self, response):
        for item in response.css('item'):
            yield {
                'title': item.css('title::text').get(),
                'link': item.css('link::text').get(),
                'description': item.css('description::text').get(),
            }

