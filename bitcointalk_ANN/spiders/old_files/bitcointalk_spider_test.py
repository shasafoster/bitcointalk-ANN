from bs4 import BeautifulSoup
import os
import urllib2
from lxml import etree
import scrapy
import add_css
import re
from collections import Counter

# Prompt the user for input (via command prompt)
#crypto_currency = raw_input("Enter the name of the crypto economic protocol: ").lower()
#print(r'Parsing ' + r'"https://coinmarketcap.com/currencies/' + crypto_currency + r'"...')

# Get base url from coinmarketcap.com
crypto_currency = 'pinkcoin'

response = urllib2.urlopen(r'https://coinmarketcap.com/currencies/' + crypto_currency)
soup = BeautifulSoup(response, 'lxml')
base_url = soup.find('a', href=True, text='Announcement')['href']

# Extract the number of pages in the bitcointalk.com thread
forum_response = urllib2.urlopen(base_url)
html_parser = etree.HTMLParser()
tree = etree.parse(forum_response, html_parser)
index_table = tree.xpath('//div[@id="bodyarea"]/table')[0]

num_pages = []
for x in index_table.xpath('./tr/td/a/text()'):
    try:
        num_pages.append(int(x))
    except ValueError:
        pass
num_pages = max(num_pages)
urls = [base_url] + [base_url[:-1] + str(int(20 * (i - 1))) for i in range(2, num_pages + 1)]


class BitcointalkSpider(scrapy.Spider):
    name = "bitcointalkTest"

    def start_requests(self):

        # Delete html file for the crypto-currency if exists
        try:
            base = r'C:\Users\Shasa\PycharmProjects\bitcointalk\bitcointalk_ANN'
            path = os.path.join(base, (crypto_currency + r'.html'))
            os.remove(path)
        except OSError:
            pass

        with open(r'./style.html', 'r') as f:
            style = f.read()
        f.close()

        with open(crypto_currency + '.html', 'a') as f:
            f.write(style)
        f.close()

        # Parse urls
        for i, url in enumerate(urls):
            yield scrapy.Request(url=url, meta={'priority': i}, callback=self.parse, )

    def parse(self, response):

        # We only want user posts (no ads, deleted posts etc)
        table = response.xpath('//div[@id="bodyarea"]/form[@id="quickModForm"]/table')[0]
        rows = list(table.xpath('./tr'))
        joined = ''.join([str(row) for row in rows])
        results = re.findall(r'<tr class="[\w]+">', joined)
        most_common_result = Counter(results).most_common()[0][0]
        most_common_class= re.findall(r'"[\w]+"', most_common_result)[0].replace('"', '')
        x_path = './tr[@class="' + most_common_class + '"]'
        posts = table.xpath(x_path)

        filename = crypto_currency + '.html'
        with open(filename, 'a') as f:
            for post in posts:
                f.write(BeautifulSoup(post.extract(), 'lxml').encode('utf8'))
        f.close()
        self.log('Saved file %s' % filename)
