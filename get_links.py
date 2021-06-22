from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector


class Moto(Item):
    clase = Field()
    link = Field()


class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 3000,
        'CONCURRENT_REQUESTS': 16,
        'FEED_EXPORT_FIELDS': ['clase', 'link']
    }

    allowed_domains = ['motos.mercadolibre.com.ar']

    start_urls = ["https://motos.mercadolibre.com.ar/naked",
                  "https://motos.mercadolibre.com.ar/scooters",
                  "https://motos.mercadolibre.com.ar/enduro",
                  "https://motos.mercadolibre.com.ar/deportivas",
                  "https://motos.mercadolibre.com.ar/calle",
                  "https://motos.mercadolibre.com.ar/touring",
                  "https://motos.mercadolibre.com.ar/cross",
                  "https://motos.mercadolibre.com.ar/cuatriciclos",
                  "https://motos.mercadolibre.com.ar/chopper"
                  ]

    download_delay = 1

    rules = (
        Rule(
            LinkExtractor(
                allow=r'_Desde_\d+$'
            ), follow=True, callback='parse_items'),
    )

    def parse_items(self, response):

        sel = Selector(response)
        links = sel.xpath('//div[@class="slick-slide slick-active"]/img')
        clase = sel.xpath('//h1[@class="ui-search-breadcrumb__title"]/text()').get()

        for link in links:
            item = ItemLoader(Moto(), link)
            item.add_value('clase', clase)
            item.add_xpath('link', './/@data-src')

            yield item.load_item()
