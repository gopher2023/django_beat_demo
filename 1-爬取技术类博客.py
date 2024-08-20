import requests
from bs4 import BeautifulSoup

res = requests.get('https://www.cnblogs.com/')
# print(res.text)
soup = BeautifulSoup(res.text, 'html.parser')
# 查找：-文章标题-文章作者-文章url地址-文章摘要
# 找到所有文章
article_list=soup.find_all(name='article',class_='post-item')
# 循环一个个文章
for article in article_list:
    title=article.find(name='a',class_='post-item-title').text
    url=article.find(name='a',class_='post-item-title').attrs.get('href')
    author=article.find(name='a',class_='post-item-author').span.text
    desc=article.find(name='p',class_='post-item-summary').text.strip()
    print(f'''
    文章名字：{title}
    文章地址：{url}
    文章作者：{author}
    文章摘要：{desc}
    ''')
    # 保存到数据库中
    # 去重，不能有重复


