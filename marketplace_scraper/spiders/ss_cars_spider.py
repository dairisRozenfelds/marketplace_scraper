import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.conf import settings
from marketplace_scraper.items import SsCarsItemDeep
from marketplace_scraper.items import SsCarsItem
from datetime import datetime

class SsSpider(scrapy.Spider):
    name = "ss_cars"
    urls = [
        'https://www.ss.com/lv/transport/cars/bmw/',
        'https://www.ss.com/lv/transport/cars/audi/'
    ]
    dropCollections = [
        'bmw',
        'audi'
    ]

    def __init__(self, deepSearch = False):
        self.deepSearch = deepSearch

    def start_requests(self):
        for url in self.urls:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request

    def concat_list(self, passedList: list):
        return ''.join(passedList).replace('  ', ' ')

    def entryParse(self, response):
        mainContent = response.css('#content_main_div #msg_div_msg')

        price = self.concat_list(mainContent.css('#tdo_8').xpath('.//text()').extract()).replace('€', '').replace(' ', '')
        if price.isnumeric():
            item = SsCarsItemDeep()
            group = response.request.url.split('/')[-3]
            item['group'] = group
            name = self.concat_list(mainContent.css('#tdo_31').xpath('.//b/text()').extract()).split()
            if (len(name) >= 2):
                item['name'] = name[0]
                item['model'] = name[1]
            else:
                item['name'] = name
                item['model'] = name
            item['year'] = self.concat_list(mainContent.css('#tdo_18').xpath('.//text()').extract())
            item['engine'] = self.concat_list(mainContent.css('#tdo_15').xpath('.//text()').extract())
            item['gearbox'] = self.concat_list(mainContent.css('#tdo_35').xpath('.//text()').extract())
            item['mileage'] = self.concat_list(mainContent.css('#tdo_16').xpath('.//text()').extract()).replace(' ', '')
            item['color'] = self.concat_list(mainContent.css('#tdo_17').xpath('.//text()').extract())
            item['TA'] = self.concat_list(mainContent.css('#tdo_223').xpath('.//text()').extract())
            item['price'] = price
            item['date_added'] = datetime.strptime(self.concat_list(response.css('#page_main .msg_footer')[3].xpath('.//text()').extract()).replace('Datums:', '').lstrip(), '%d.%m.%Y %H:%M')
            item['url'] = response.request.url
            yield item

    def parse(self, response):
        pageTables = response.css('form#filter_frm table')
        resultTable = pageTables[2]
        rows = resultTable.xpath('.//tr')[1:]
        baseUrl = 'https://www.ss.com'

        # First row is header row
        for row in rows:
            cols = row.xpath('.//td')

            # Check if it is a commercial (commercials don't have 8 cols)
            if len(cols) >= 8:
                price = self.concat_list(cols[7].xpath('.//text()').extract())

                # Check if it is a entry where item is sold
                if price.find('pērku') == -1 and price.find('maiņai') == -1:
                    entryLink = self.concat_list(cols[2].xpath('.//a/@href').extract())
                    
                    #If deepSearch is enabled, the crawler goes through every link to gather more detailed info
                    if self.deepSearch:
                        entryRequest = scrapy.Request(baseUrl + entryLink, callback = self.entryParse)
                        yield entryRequest
                    else:
                        item = SsCarsItem()
                        group = response.request.url.split('/')[-2]

                        if self.concat_list(cols[3].xpath('.//text()').extract()):
                            model = self.concat_list(cols[3].xpath('.//text()').extract())
                            year = self.concat_list(cols[4].xpath('.//text()').extract())
                            engine = self.concat_list(cols[5].xpath('.//text()').extract())
                            mileage = self.concat_list(cols[6].xpath('.//text()').extract())
                        else:
                            model = self.concat_list(cols[3].xpath('.//b/text()').extract())
                            year = self.concat_list(cols[4].xpath('.//b/text()').extract())
                            engine = self.concat_list(cols[5].xpath('.//b/text()').extract())
                            mileage = self.concat_list(cols[6].xpath('.//b/text()').extract())
                        
                        item['group'] = group
                        item['name'] = group.capitalize()
                        item['model'] = model
                        item['year'] = year
                        item['engine'] = engine
                        item['mileage'] = mileage.replace('tūkst.', '000').replace(' ', '').replace('-', '')
                        item['price'] = price.strip().strip('€').replace(' ', '').replace(',', '')
                        item['url'] = baseUrl + entryLink
                        yield item
            else:
                break

        # Extract the last items href from the navigation bar (it's the next page button)
        pageRequest = scrapy.Request(baseUrl + pageTables[-2].xpath('.//a[@name="nav_id"]')[-1].xpath('@href').extract()[0], callback = self.parse)
        yield pageRequest
