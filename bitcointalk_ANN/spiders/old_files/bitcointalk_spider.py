from bs4 import BeautifulSoup
import os
import urllib2
from lxml import etree
import scrapy
import add_css

# Prompt the user for input (via command prompt)
crypto_currency = raw_input("Enter the name of the crypto economic protocol: ").lower()
print(r'Parsing ' + r'"https://coinmarketcap.com/currencies/' + crypto_currency + r'"...')

# Get base url from coinmarketcap.com
url = r'https://coinmarketcap.com/currencies/' + crypto_currency
response = urllib2.urlopen(url)
soup = BeautifulSoup(response, 'lxml')
base_url = soup.find('a', href=True, text='Announcement')['href']

# Extract the number of pages in the bitcointalk.com thread
forum_response = urllib2.urlopen(base_url)
html_parser = etree.HTMLParser()
tree = etree.parse(forum_response, html_parser)
table = tree.xpath('//div[@id="bodyarea"]/table')[0]

num_pages = []
for x in table.xpath('./tr/td/a/text()'):
    try:
        num_pages.append(int(x))
    except ValueError:
        pass
num_pages = max(num_pages)
urls = [base_url] + [base_url[:-1] + str(int(20 * (i - 1))) for i in range(2, num_pages + 1)]
urls = urls[:2]

# Extract the CSS pages
add_css.write_css(crypto_currency, base_url)

class BitcointalkSpider(scrapy.Spider):
    name = "bitcointalk"

    def start_requests(self):

        # Delete html file for the crypto-currency if exists
        try:
            base = r'C:\Users\Shasa\PycharmProjects\bitcointalk\bitcointalk_ANN'
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
            #f.write(BeautifulSoup(table.extract(), 'lxml').encode('utf8'))

            posts = table.xpath('./tr')
            for post in posts:

            # x=list(table.xpath('./tr'))
            # x
            # re.findall(r'<tr class="[\w]+">',X)
            # f.write(BeautifulSoup(post.extract(),'lxml').encode('utf8'))
        f.close()
        self.log('Saved file %s' % filename)
