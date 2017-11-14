from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from bitcointalk_ANN.helper import *


def script():
    num_of_thread_pages, crypto_currency = get_urls()

    process = CrawlerProcess(get_project_settings())
    process.crawl('bitcointalk')
    process.start()  # the script will block here until the crawling is finished

    num_of_scraped_pages = merge(crypto_currency)

    print_log(crypto_currency, num_of_thread_pages, num_of_scraped_pages)


script()

