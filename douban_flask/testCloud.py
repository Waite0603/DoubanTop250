import jieba  # 分词
from matplotlib import pyplot as plt  # 绘图，数据可视化
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算
import sqlite3  # 数据库


# 删除词云中的单个字符
def wordtowords(string):
    finalStr = ""
    for i in range(len(string)):  # 遍历每个字符
        try:
            if string[i - 1] == " " and string[i + 1] == " ":  # 若此字符前后都为空白，则判断为单字符，丢弃
                continue
        except Exception as e:  # 第一个和最后一个字符的判断会越界
            print(e)
        finalStr += string[i]  # 保存通过判断的字符
    return finalStr


# 准备词云所需的文字（词）
con = sqlite3.connect('movie.db')
cur = con.cursor()
sql = 'select instroduction from movie250'
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
cur.close()
con.close()

# 分词
cut = jieba.cut(text)
string = ' '.join(cut)
words = wordtowords(string)
# print(words)


img = Image.open(r'.\static\assets\img\tree.jpg')  # 打开遮罩图片
img_array = np.array(img)  # 将图片转换为数组
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path="msyh.ttc"  # 字体所在位置：C:\Windows\Fonts
)
wc.generate_from_text(words)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')  # 是否显示坐标轴

# 输出词云图片到文件
plt.savefig(r'.\static\assets\img\word.jpg', dpi=500)

plt.show()  # 显示生成的词云图片
