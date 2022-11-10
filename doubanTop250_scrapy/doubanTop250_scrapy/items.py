import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 电影评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()
    # 格言
    quote = scrapy.Field()
    pass
