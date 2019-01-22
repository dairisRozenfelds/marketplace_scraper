import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.conf import settings
from marketplace_scraper.items import AutopliusCarsItem

class AutopliusSpider(scrapy.Spider):
    name = "autoplius"
    urls = [
        'https://en.autoplius.lt/ads/used-cars/bmw',
        'https://en.autoplius.lt/ads/used-cars/audi'
    ]
    dropCollections = [
        'bmw_autoplius',
        'audi_autoplius'
    ]

    def start_requests(self):
        urls = self.urls
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request

    def concat_list(self, passedList: list):
        return ''.join(passedList).replace('  ', ' ')

    def parse(self, response):
        rows = response.css('.announcement-item')
        baseUrl = 'https://en.autoplius.lt'

        for row in rows:
            body = row.css('.announcement-body')
            # Result: ['BMW X1', '2.0 l.', 'suv / off-road']
            title = self.concat_list(body.css('.announcement-title::text').extract()).strip().split(',')
            # Result: ['BMW', 'X1']
            fullName = title[0].split(' ', 1)
            name = fullName[0]
            model = fullName[1]
            params = body.css('.announcement-parameters')
            group = response.request.url.split('/')[-1].split('?')[0]
            price = self.concat_list(body.css('.announcement-pricing-info').xpath('.//strong/text()').extract()).replace(' ', '').replace('€', '')
            if price.isnumeric():
                item = AutopliusCarsItem()
                item['group'] = group + '_autoplius'
                item['name'] = name
                item['model'] = model
                item['year'] = self.concat_list(params.xpath('.//span[contains(@title, "Date of manufacture")]/text()').extract()).split('-')[0]
                if len(title) >= 2:
                    item['engine'] = title[1].replace(' l.', '')
                else:
                    item['engine'] = ''
                item['mileage'] = self.concat_list(params.xpath('.//span[contains(@title, "Mileage")]/text()').extract()).replace(' ', '').replace('km', '')
                item['price'] = price
                item['url'] = self.concat_list(row.xpath('.//@href').extract())
                yield item
            
        #Go to next page
        if (self.concat_list(response.css('.paging-bot .pagination li.next a.next').xpath('.//@href').extract())):            
            pageRequest = scrapy.Request(baseUrl + self.concat_list(response.css('.paging-bot .pagination li.next a.next').xpath('.//@href').extract()), callback = self.parse)
            yield pageRequest
