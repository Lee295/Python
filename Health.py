from lxml import etree
import requests
import pymysql

URL = 'http://jiankang.cctv.com/?spm=C94212.P4YnMod9m2uD.0.0'
headers = {
    'User': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/77.0.3865.90 Safari/537.36'
}
response = requests.get(URL, headers=headers)
response.encoding = 'utf-8'
html = etree.HTML(response.text)
result = []
content = html.xpath('//div[@class="ELMT7SC9i3MXEtNzziqaUahj190425"]//li[@class="sbl"]')
for news in content:
    data = {}
    data['title'] = news.xpath('a/text()')
    data['url'] = news.xpath('a/@href')
    result.append(data)

table = 'health'
for i in range(len(result)):
    keys = ','.join(result[i].keys())
    values = ','.join(['%s'] * len(result[i]))
    db = pymysql.connect(host='localhost', user='root', password='045094', port=3306, charset='utf8', db='medicine')
    cursor = db.cursor()
    sql = 'INSERT INTO {table}({keys}) VALUES({values})'.format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(result[i].values())):
            # print('Successful')
            db.commit()
    except Exception as e:
        # print('Failed')
        print(e)
        db.rollback()
db.close()
