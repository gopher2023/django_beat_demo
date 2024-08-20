
import requests
from bs4 import BeautifulSoup
res = requests.get('https://pic.netbian.com/tupian/33929.html')
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
        with open('./img/%s'%name, 'wb') as f:
            for line in res1.iter_content():
                f.write(line)
    except Exception as e:
        continue