# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from bs4 import BeautifulSoup


class PostPipeline(object):

    def process_item(self, item, spider):

        filename = r'C:/Users/Shasa/PycharmProjects/bitcointalk/bitcointalk_ANN/bitcointalk_ANN/pages' \
                   + '/' + str(item['page_number']) + '.html'
        with open(filename, 'wb') as f:
            soup = BeautifulSoup(item['posts'])
            f.write(soup.prettify(encoding='utf-8'))
            print('Saving page ' + str(item['page_number']))
        f.close()


