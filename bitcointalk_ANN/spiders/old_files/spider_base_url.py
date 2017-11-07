import pickle
from bs4 import BeautifulSoup
import urllib2
from lxml import etree
import scrapy
from spider_bitcointalk import BitcointalkSpider
from scrapy.crawler import CrawlerProcess

# Prompt the user for input (via command prompt)
name = raw_input("Enter the name of the crypto economic protocol: ")

# Get base url from coinmarketcap.com
url = r'https://coinmarketcap.com/currencies/' + name
response = urllib2.urlopen(url)
soup = BeautifulSoup(response, 'lxml')
base_url = soup.find('a', href=True, text='Announcement')['href']

# Extract the number of pages in the bitcointalk thread
response = urllib2.urlopen(base_url)
html_parser = etree.HTMLParser()
tree = etree.parse(response, html_parser)
table = tree.xpath('//div[@id="bodyarea"]/table')[0]
num_pages = max([int(x) for x in table.xpath('./tr/td/a/text()')])

# Create list of page urls in thread for spider to parse and then pickle the list
urls = [base_url] + [base_url[:-1] + str(int(20 * (i - 1))) for i in range(2, num_pages + 1)]
urls = urls[:2]
output = open('urls.pkl', 'wb')
pickle.dump(urls, output)
output.close()

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

# Run spider
process.crawl(BitcointalkSpider)
process.start()