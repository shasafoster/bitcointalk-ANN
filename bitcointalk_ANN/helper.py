from bs4 import BeautifulSoup
from urllib.request import urlopen
from lxml import etree
import pickle
import os
import glob
import re


def get_urls():
    """
    Extracts the urls of a bitcointalk [ANN] thread to be parsed and downloaded
    :return: Name of entered crpyto currency, Urls of pages in bitcointalk [ANN] thread
    """

    # Delete all files in pages directory
    files = glob.glob(r'C:/Users/Shasa/PycharmProjects/bitcointalk/bitcointalk_ANN/bitcointalk_ANN/pages/*')
    for f in files:
        os.remove(f)
    try:
        os.remove(r'C:/Users/Shasa/PycharmProjects/bitcointalk/bitcointalk_ANN/crawl.log')
    except WindowsError:
        pass

    # Prompt the user for input (via command prompt)
    print('')
    crypto_currency = input("Enter the name of the crypto economic protocol: ").lower()
    print(r'Parsing ' + r'"https://coinmarketcap.com/currencies/' + crypto_currency + r'"...')
    print('')
    print('')

    response = urlopen(r'https://coinmarketcap.com/currencies/' + crypto_currency)
    soup = BeautifulSoup(response, 'lxml')
    base_url = soup.find('a', href=True, text='Announcement')['href']

    print('The url of the first bitcointalk [ANN] thread is...')
    print(base_url)
    print('')
    print('')

    # Extract the number of pages in the bitcointalk.com thread
    forum_response = urlopen(base_url)
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

    print('This bitcointalk thread has ' + str(num_pages) + ' pages.')
    print('')
    print('')

    with open('./bitcointalk_ANN/spiders/urls.pickle', 'wb') as handle:
        pickle.dump(urls, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return num_pages, crypto_currency


def merge(crypto_currency):

    # Delete html file for the crypto-currency if exists
    try:
        base = r'C:\Users\Shasa\PycharmProjects\bitcointalk\bitcointalk_ANN'
        path = os.path.join(base, (crypto_currency + r'.html'))
        os.remove(path)
    except OSError:
        pass

    # Read in style html
    with open(r'C:/Users/Shasa/PycharmProjects/bitcointalk/bitcointalk_ANN/bitcointalk_ANN/style.html', 'r') as f:
        style = f.read()
    f.close()

    # Read in all .html files of the posts
    page_paths = glob.glob('C:/Users/Shasa/PycharmProjects/bitcointalk/bitcointalk_ANN/bitcointalk_ANN/pages/*.html')
    page_paths = sorted(page_paths)

    # Add style html to crypto-currency html doc
    with open("C:/Users/Shasa/Dropbox/ANN/" + crypto_currency + ".html", "a", encoding="utf-8") as main:
        main.write("<html>")
        main.write(style)

        main.write("<body>")
        for path in page_paths:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                main.write(content)
            f.close()
        main.write("</body>")
        main.write("</html>")
    main.close()


#def print_log():
 #   with open('crawl.log', 'r', encoding='utf8') as f:
  #      for line in f:
   #         if "item_scraped_count': " in line:
    #            count = re.findall(r"': [\d]+", line)
     #           return count[0].replace("'", "").replace(":", "")
