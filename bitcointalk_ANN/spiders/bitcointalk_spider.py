import scrapy
from bs4 import BeautifulSoup
import os
import pickle

# Read in from pickled file
pkl_file = open(r'C:\Users\Shasa\Documents\Projects\bitcointalk_ANN\bitcointalk_ANN\name_urls.pkl', 'rb')
name_urls = pickle.load(pkl_file)
pkl_file.close()
crypto_currency = name_urls[0]
urls = name_urls[1:2]  # *****Note*****


class BitcointalkSpider(scrapy.Spider):
    name = "bitcointalk"

    def start_requests(self):

        # Delete html file for the crypto-currency if exists
        try:
            base = r'C:\Users\Shasa\Documents\Projects\bitcointalk_ANN'
            path = os.path.join(base, (crypto_currency + r'.html'))
            os.remove(path)
        except OSError:
            pass

        # Parse urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # The posts from the webpage
        table = response.xpath('//div[@id="bodyarea"]/form[@id="quickModForm"]/table')[0]
        # posts = table.xpath('./tr')

        filename = crypto_currency + '.html'
        with open(filename, 'a') as f:
            f.write(BeautifulSoup(table.extract(), 'lxml').encode('utf8'))
            # for post in posts:
            # f.write(BeautifulSoup(post.extract(),'lxml').encode('utf8'))
        f.close()
        self.log('Saved file %s' % filename)