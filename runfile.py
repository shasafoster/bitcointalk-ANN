from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from bitcointalk_ANN.helper import *


def script():
    num_pages, crypto_currency = get_urls()
    process = CrawlerProcess(get_project_settings())
    process.crawl('bitcointalk')
    process.start()  # the script will block here until the crawling is finished
    merge(crypto_currency)
    count = print_log()
    print('')
    print '********************************************'
    print('             ' + str(count) + ' pages scraped')
    print '********************************************'


script()

