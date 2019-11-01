'''
输入关键词
爬取百度百科第一段的简介
爬取百度图片前三十张图片
'''

import threading
import urllib.request
from urllib.parse import quote
import urllib.parse
import re
import os
from lxml import etree


class BaikeAndImg:
    global headers  # 定义全局变量headers
    # 字典headers 浏览器标识
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
        "referer": "https://image.baidu.com"
    }

    # 创建函数，用于爬取百度百科相关
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
        # 创建文本文档并打开，保存爬取的信息
        with open('Medicine.txt', 'a', encoding='utf-8') as f:
            f.write(content + '\n') # 写入关键词，并换行
            f.writelines(result)    # 写入爬取的结果
            f.writelines('\n\n')    # 两次换行
        f.close()   # 关闭文档

    # 创建爬取图片的函数
    def medicine_img(content):
        last_dir = "E:/Python/Medicine/IMG/"    # 创建IMG文件夹
        dir = "E:/Python/Medicine/IMG/" + content   # 在IMG文件夹下，创建以关键词content命名的文件夹，用于保存爬取的图片
        if os.path.exists(last_dir):    # 判断IMG文件夹是否存在
            if os.path.exists(dir):     # 若IMG文件夹存在，判断content文件夹是否存在，若存在，输出提示
                print("文件夹已经存在")
            else:                       # 若不存在，创建content文件夹，并输出提示
                os.mkdir(dir)
                print(dir + "已经创建成功")
        else:                           
            os.mkdir(last_dir)          # 若IMG文件夹不存在，创建IMG文件夹
            if os.path.exists(dir):     # 判断content文件夹是否存在，若存在，输出提示
                print("文件夹已经存在")
            else:                       # 若不存在，创建content文件夹，并输出提示
                os.mkdir(dir)
                print(dir + "已经创建成功")
                
        keyword1 = quote(content, encoding="utf-8") # 将关键词content传入keyword1，URL编码为 utf-8
        
        '''
        拆分百度图片网址
        前半段"http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word="
        是，利用百度图片搜索时的通用地址， keyword1是quote函数传入的关键词content
        '''
        url = "http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=" + keyword1
        
        '''
        url.request模块提供了最基本的构造HTTP请求的方法，利用它可以模拟成浏览器的一个请求发送过程
        
        利用Request()方法构造一个发送请求。Request()参数包括，url(请求网址，必传参数)，headers请求头
        利用urlopen()方法，实现网页的GET请求抓取
        利用read()方法得到返回的网页内容
        decode()方法规定编码格式为utf-8
        '''
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
