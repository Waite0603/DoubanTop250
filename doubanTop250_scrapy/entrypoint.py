from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'douban_top250', '-o', 'doubanauto.csv'])