import scrapy
import pickle
import re
from collections import Counter
from bitcointalk_ANN.items import PostsItem


with open('./bitcointalk_ANN/spiders/urls.pickle', 'rb') as handle:
    urls = pickle.load(handle)


class BitcointalkSpider(scrapy.Spider):
    name = "bitcointalk"

    def start_requests(self):
        # Parse urls
        for i, url in enumerate(urls):
            yield scrapy.Request(url=url, callback=self.parse,  meta={'page_number': i}, dont_filter=True)

    def parse(self, response):

        # We only want user posts (no ads, deleted posts etc)
        table = response.xpath('//div[@id="bodyarea"]/form[@id="quickModForm"]/table')[0]
        rows = list(table.xpath('./tr'))
        joined = ''.join([str(row) for row in rows])
        results = re.findall(r'<tr class="[\w]+">', joined)
        most_common_result = Counter(results).most_common()[0][0]
        most_common_class= re.findall(r'"[\w]+"', most_common_result)[0].replace('"', '')
        x_path = './tr[@class="' + most_common_class + '"]'
        post_list = table.xpath(x_path)
        posts = ''.join([post.extract()for post in post_list])

        # Create PostsItem item and assign variables
        posts_item = PostsItem()
        posts_item['page_number'] = response.request.meta['page_number']
        posts_item['posts'] = posts
        yield posts_item


