## 介绍

### douban_ResToSqlite

使用 urllib.request 获取网页源代码, 用正则抓取豆瓣资源并保存为为 Sqlite 数据库 / Xls 表格

### doubanTop250_scrapy

使用 scrapy 框架抓取豆瓣 Top250 豆瓣资源并保存为为 Csv 文件

### douban_flask

使用 flask 框架搭建豆瓣资源网站, 从 Sqlite 数据库中读取数据, 使用 wordcloud, echarts 进行可视化, 并使用 jinja2 模板引擎渲染网页, 使用 bootstrap 框架美化网页

## 环境安装

```shell
python v3.10

pip install -r requirements.txt
```