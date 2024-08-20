# 注册任务
import time

from celery import shared_task

### 写个类，继承 Task，写方法
from celery import Task

from django.core.mail import send_mail
from django.conf import settings


class SendEmailTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        # 任务执行成功，会执行这个
        info = f'爬虫任务成功-- 任务id是:{task_id} , 参数是:{args} , 执行成功 !'
        # 发送邮件--》django中发送邮件
        send_mail('celery监控成功告警', info, settings.EMAIL_HOST_USER, ['616564099@qq.com'])

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # 任务执行失败，会执行这个
        info = f'爬虫任务失败-- 任务id是:{task_id} , 参数是:{args} , 执行失败，请去flower中查看原因 !'
        # 发送邮件--》django中发送邮件
        send_mail('celery监控爬虫失败告警', info, settings.EMAIL_HOST_USER, ['616564099@qq.com'])

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # 任务执行重试，会执行这个
        print('重试了！！！')


# 以后使用shared_task 替换掉 app.task

# 任务函数
@shared_task
def add(a, b):
    print(f'-------->  {a} + {b} = {a+b}')
    return a + b


@shared_task
def send_email(to_user):
    time.sleep(2)
    return '发送邮件成功:%s' % to_user


###爬取技术博客#####
import requests
from bs4 import BeautifulSoup
from .models import Article
from redis import Redis


@shared_task(base=SendEmailTask, bind=True)  # 只要执行它成功或失败，都会给 616564099@qq.com发送邮件
def crawl_cnblogs(self):
    # 拿到redis链接
    conn = Redis(host='127.0.0.1', port=6379)
    res = requests.get('https://www.cnblogs.com/')
    soup = BeautifulSoup(res.text, 'html.parser')
    # 查找：-文章标题-文章作者-文章url地址-文章摘要
    # 找到所有文章
    article_list = soup.find_all(name='article', class_='post-item')
    # 循环一个个文章
    for article in article_list:
        title = article.find(name='a', class_='post-item-title').text
        url = article.find(name='a', class_='post-item-title').attrs.get('href')
        author = article.find(name='a', class_='post-item-author').span.text
        desc = article.find(name='p', class_='post-item-summary').text.strip()
        print(f'''
        文章名字：{title}
        文章地址：{url}
        文章作者：{author}
        文章摘要：{desc}
        ''')
        # 去重，不能有重复,如果重复了，就不存到数据库中了---》集合可以去重--》redis集合去重-->根据url去重
        # 只要redis的urls的这个集合中，有了这个地址，我们就不存了--》去重了

        res = conn.sadd('urls', url)
        if res:  # 返回1 表示放进集合中了，表示集合中没有，存数据库   返回0，表示集合中有过，不存了
            # 保存到数据库中--》创建一个Article的数据表
            Article.objects.create(title=title, url=url, author=author, desc=desc)

    return True



### 爬取图片
import os
# 爬取美女图片
@shared_task(base=SendEmailTask, bind=True)
def crawl_photo(self,url):
    res = requests.get(url)
    res.encoding = 'gbk'
    soup = BeautifulSoup(res.text, 'html.parser')
    ul = soup.find('ul', class_='clearfix')
    img_list = ul.find_all(name='img', src=True)
    for img in img_list:
        try:
            url = img.attrs.get('src')
            if not url.startswith('http'):
                url = 'https://pic.netbian.com' + url
            print(url)
            res1 = requests.get(url)
            name = url.split('-')[-1]
            with open(os.path.join(settings.BASE_DIR,'img',name), 'wb') as f:
                for line in res1.iter_content():
                    f.write(line)
        except Exception as e:
            continue
