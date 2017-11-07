from ANN_info import BASE_URL
import scrapy
import pickle


class UrlsSpider(scrapy.Spider):
    name = "urls"

    def start_requests(self):

        yield scrapy.Request(url=BASE_URL, callback=self.parse)

    def parse(self, response):

        # Extract the number of pages in the bitcointalk thread
        table = response.xpath('//div[@id="bodyarea"]/table')[0]
        num_pages = max([int(x) for x in table.xpath('./tr/td/a/text()').extract()])


        # Create list of pages in thread for spider to parse and then pickle the list
        urls = [BASE_URL] + [BASE_URL[:-1] + str(int(20 * (i - 1))) for i in range(2, num_pages + 1)]
        urls = urls[:2]
        output = open('urls.pkl', 'wb')
        pickle.dump(urls, output)
        output.close()