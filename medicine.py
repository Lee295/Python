import threading
import urllib.request
from urllib.parse import quote
import urllib.parse
import re
import os
from lxml import etree


class Medicine:
    global headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
        "referer": "https://image.baidu.com"
    }

    def medicine_introduction(content):
        # 请求地址
        url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)
        # 利用请求地址和请求头部构造请求对象
        req = urllib.request.Request(url=url, headers=headers, method='GET')
        # 发送请求，获得响应
        response = urllib.request.urlopen(req)
        # 读取响应，获得文本
        text = response.read().decode('utf-8')
        # 构造 _Element 对象
        html = etree.HTML(text)
        # 使用 xpath 匹配数据，得到匹配字符串列表
        sen_list = html.xpath('//div[contains(@class,"lemma-summary") or contains(@class,"lemmaWgt-lemmaSummary")]//text()')
        # 过滤数据，去掉空白
        sen_list_after_filter = [item.strip('\n') for item in sen_list]
        # 将字符串列表连成字符串并返回
        result = ''.join(sen_list_after_filter)
        with open('Medicine.txt', 'a', encoding='utf-8') as f:
            f.write(content + '\n')
            f.writelines(result)
            f.writelines('\n\n')
        f.close()

    def medicine_img(content):
        last_dir = "E:/Python/Medicine/IMG/"
        dir = "E:/Python/Medicine/IMG/" + content
        if os.path.exists(last_dir):
            if os.path.exists(dir):
                print("文件夹已经存在")
            else:
                os.mkdir(dir)
                print(dir + "已经创建成功")
        else:
            os.mkdir(last_dir)
            if os.path.exists(dir):
                print("文件夹已经存在")
            else:
                os.mkdir(dir)
                print(dir + "已经创建成功")
        keyword1 = quote(content, encoding="utf-8")
        url = "http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=" + keyword1
        req = urllib.request.Request(url, headers=headers)
        f = urllib.request.urlopen(req).read().decode("utf-8")
        key = r'thumbURL":"(.+?)"'
        key1 = re.compile(key)
        num = 1
        for string in re.findall(key1, f):
            f_req = urllib.request.Request(string, headers=headers)
            f_url = urllib.request.urlopen(f_req).read()
            fs = open(dir + "/" + content + str(num) + ".jpg", "wb+")
            fs.write(f_url)
            fs.close()
            num += 1


if __name__ == '__main__':
    while True:
        content = input('查询词语：')
        thead_int = threading.Thread(target=Medicine.medicine_introduction(content))
        thead_img = threading.Thread(target=Medicine.medicine_img(content))
        thead_int.start()
        thead_int.join()
        thead_img.start()
        print("查询完成！")
