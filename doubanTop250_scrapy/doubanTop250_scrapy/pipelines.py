# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class Doubantop250ScrapyPipeline:
    def open_spider(self, spider):
        print('爬虫开始')
        self.db = open('./豆瓣250排行榜.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 接收值
        title = item['title']
        message = item['message']
        score = item['score']
        quote = item['quote']

        db_dict = {
            '电影名': title,
            '评分': score,
            '电影金句': quote
        }
        # 保存数据
        db_json = json.dumps(db_dict, ensure_ascii=False, indent=2)
        self.db.write(db_json)
        return item

    def close_spider(self, spider):
        print('爬虫结束')
        self.db.close()
