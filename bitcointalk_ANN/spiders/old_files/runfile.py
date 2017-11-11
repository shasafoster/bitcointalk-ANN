import pickle
from lxml import etree
from fetch_css import *
import urllib2
from bs4 import BeautifulSoup
import subprocess

# Prompt the user for input (via command prompt)
crypto_currency = raw_input("Enter the name of the crypto economic protocol: ")

# Get base url for the bitcointalk [ANN] from coinmarketcap.com
url = r'https://coinmarketcap.com/currencies/' + crypto_currency
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
name_urls = [crypto_currency] + [base_url] + [base_url[:-1] + str(int(20 * (i - 1))) for i in range(2, num_pages + 1)]
path = r'C:\Users\Shasa\Documents\Projects\bitcointalk_ANN\bitcointalk_ANN\name_urls.pkl'
output = open(path, 'wb')
pickle.dump(name_urls, output)
output.close()

# Extract the CSS of the bitcointalk webpage and write to file
'---------------------------'
print('Extracting CSS...')
'---------------------------'
write_css(crypto_currency, base_url)

# python 3.5+
# subprocess.run(['scrapy crawl bitcointalk'])
