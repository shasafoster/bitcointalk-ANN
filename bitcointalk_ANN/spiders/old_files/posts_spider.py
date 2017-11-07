import scrapy
import os


class PostsSpider(scrapy.Spider):
    name = "posts"

    def start_requests(self):
        try:
            path = r"C:\Users\Shasa\Documents\Projects\bitcointalk_ANN\posts.txt"
            os.remove(path)
        except OSError:
            pass

        urls = [
            'https://bitcointalk.org/index.php?topic=421615.0'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        filename = 'post.txt'
        with open(filename, 'a') as f:

            # get title of ANN thread and write
            title = response.xpath('//title/text()').extract_first()
            f.write(title.encode('utf8'))
            f.write("\n")

            # extract table of posts
            table = response.xpath('//div[@id="bodyarea"]/form[@id="quickModForm"]/table')[0]

            # Get the info on the posters
            poster_info = table.css('.poster_info')

            # Get the info on the post
            post_info = table.css('.td_headerandpost n.post')

            for s in poster_info:
                username = s.css('a::text').extract()[0]
                user_info = s.css('.smalltext').xpath('./text()').re('[ \w . \w ]+')[:3]


                # write username, rank level, user activity
                if any(c.isalpha() for c in username):
                    f.write(username.encode('utf8'))
                    f.write(',')

                    for ss in user_info:
                        f.write(ss.encode('utf8'))
                        f.write(',')
                    f.write("\n")

        self.log('Saved file %s' % filename)
