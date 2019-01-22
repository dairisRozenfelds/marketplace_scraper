# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy import log

class SsCarsPipeline(object):
    latestDates = {}

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]

    def open_spider(self, spider):
        for group in spider.dropCollections:
            self.db[group].drop()
        
    def process_item(self, item, spider):
        self.db[item['group']].insert(dict(item))
        log.msg(str(item['name']) + " added to database.", level=log.DEBUG, spider=spider)

        # For MySQL #
        # for key, value in item.items():
        #     print(key)
        #     if len(item.items()) - 1 != i:
        #         queryValues += '\"' + ''.join(value) + '\", '
        #     else:
        #         queryValues += '\"' + ''.join(value) + '\"'
        #     i += 1
        # query = f"""INSERT INTO {self.tableName} (name, model, year, engine, gearbox, mileage, color, TA, price, date_added, url) VALUES ({queryValues})"""
        # self.cursor.execute(query)
        return item

    # def close_spider(self, item, spider):
    #     self.conn.commit()
        
