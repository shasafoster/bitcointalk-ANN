import scrapy
import os
import pickle


class BitcointalkSpider(scrapy.Spider):
    name = "bitcointalk"

    def start_requests(self):
        # Delete text file if exists
        try:
            path = os.path.join(BASE_DIR, (CRYPTO_NAME + r'.html'))
            os.remove(path)
        except OSError:
            pass

        pkl_file = open('urls.pkl','rb')
        urls = pickle.load(pkl_file)
        urls = [urls[0]]
        pkl_file.close()

        # Parse urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # The posts from the webpage
        table = response.xpath('//div[@id="bodyarea"]/form[@id="quickModForm"]/table')[0]
        posts = table.xpath('./tr')


        filename = CRYPTO_NAME + '.html'
        with open(filename, 'a') as f:
            f.write(BeautifulSoup(table.extract(), 'lxml').encode('utf8'))
            #for post in posts:
             #   f.write(BeautifulSoup(post.extract(),'lxml').encode('utf8'))
        f.close()
        self.log('Saved file %s' % filename)