import re  # 正则表达式，进行文字匹配
import sqlite3  # 进行SQLite数据库操作
import urllib.error  # 制定URL，获取网页数据
import urllib.request

import xlwt  # 进行excel操作
from bs4 import BeautifulSoup  # 网页解析，获取数据


def main():
    # ctrl+/：多行注释
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist = getDate(baseurl)
    dbpath = "movie.db"
    # 3.保存数据
    saveData2DB(datalist, dbpath)


# region 正则表达式
# 影片详情链接规则  r:不把\符号进行转义
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串的模式）
# 影片图片
findImgSrc = re.compile(r'img.*src="(.*?)"', re.S)  # re.S:让换行符包含在字符中
# 影片片名
findTiele = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 影片评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 影片概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# endregion

# 爬取网页
def getDate(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息函数
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到得网页源码

        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求得字符串，形成列表
            data = []  # 保存一部电影得所有信息
            item = str(item)

            # region 提取
            # 添加链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)

            # 添加图片
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)

            # 添加片名
            titles = re.findall(findTiele, item)  # 片名可能只有一个中文名，没有外国名
            if len(titles) == 2:
                ctitle = titles[0]  # 添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 去掉无关的符号
                otitle = re.sub('\s+', '', otitle)  # NBSP
                data.append(otitle)  # 添加外国名
            else:
                data.append(titles[0])
                data.append('')  # 外国名字留空

            # 添加评分
            rating = re.findall(findRating, item)[0]
            data.append(rating)

            # 添加评价人数
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)

            # 添加概述
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)
            else:
                data.append("")  # 留空

            # 添加影片相关内容
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            bd = re.sub('\s+', '',
                        bd)  # 出现NBSP是因为用正则匹配html内容的时候没有将空格去掉，以介绍introduction为例，记得加上re.sub('\s+', '', introduction)就可以了，
            data.append((bd.strip()))  # 去掉前后的空格
            # endregion

            # 把处理好的一部电影信息放入datalist
            datalist.append(data)
    return datalist


# 得到指定一个URL得网页内容
def askURL(url):
    # 模拟浏览器头部信息，向网站发送消息
    head = {
        # 用户代理：告诉浏览器，能接受的文件内容得格式
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5Build/MRA58NAppleWebKit/537.36(KHTML, like Gecko) Chrome/106.0.0.0Mobile Safari/537.36"

    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print(html)

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据(excel)
def saveDate(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接", "图片链接", "电影中文名", "影片外文名", "评分", "评价人数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 数据
    book.save(savepath)  # 保存
    print("打印成功！")


# 保存数据(sqlite)
def saveData2DB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie250(
            info_link,pic_link,cname,ename,score,rated,instroduction,info)
            values (%s)
        ''' % ",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


# 初始化数据库
def init_db(dbpath):
    sql = '''
        create table IF NOT EXISTS movie250
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        instroduction text,
        info text
        )
    '''  # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # 调用函数
    # main()
    askURL("https://movie.douban.com/top250?start=")
    print("爬取完毕")

