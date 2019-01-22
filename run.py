import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from marketplace_scraper.spiders.ss_cars_spider import SsSpider
from marketplace_scraper.spiders.autoplius_cars_spider import AutopliusSpider

process = CrawlerProcess(get_project_settings())

# Definēsim, kādus URL gribam apstaigāt SS.COM
SSurls = [
    'https://www.ss.com/lv/transport/cars/bmw/',
    'https://www.ss.com/lv/transport/cars/audi/'
]
## Šis ir nepieciešams, lai zinātu, kādas vecās kolekcijas ir jāizmet, lai netiktu sabojāta statistika
# TODO: Pārveidot, lai katrai jaunai kolekcijai pieliktu timestamp un tādā veidā tās varētu atšķirt
SSdropCollections = [
    'bmw',
    'audi'
]

# Definēsim, kādus URL gribam apstaigāt AUTOPLIUS.LT
APurls = [
    'https://en.autoplius.lt/ads/used-cars/bmw',
    'https://en.autoplius.lt/ads/used-cars/audi'
]
APdropCollections = [
    'bmw_autoplius',
    'audi_autoplius'
]

SS = SsSpider(scrapy.Spider)
AP = AutopliusSpider(scrapy.Spider)

# Ievietojam augstāk definētos URL un kolekcijas
SS.urls = SSurls
SS.dropCollections = SSdropCollections

AP.urls = APurls
AP.dropCollections = APdropCollections

process.crawl(SS)
process.crawl(AP)
process.start()