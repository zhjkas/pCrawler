import json
import logging
import random
import time
import requests
import urllib3
from fake_useragent import UserAgent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 请求网站进行下载
class DownloadRun:
    def __init__(self, filepath, execute_path, username, password, cookies):
        self.base_url = 'https://www.pixiv.net'
        self.filepath = filepath
        self.exePath = execute_path
        self.userName = username
        self.pwd = password
        self.cookies = cookies
        # useragent随机生成
        self.agent = UserAgent(verify_ssl=False).random

    @staticmethod
    def get_DL(f_url, cookie, userAgent, path, b):
        headers = {
            'user-agent': userAgent,
            'Referer': 'https://www.pixiv.net/'
        }
        pic_name = f_url[-8:]
        x = 0
        while True:
            try:
                f_url1 = f_url + '_p0.jpg'
                response = requests.get(f_url1, verify=False, headers=headers, cookies=cookie)
                logging.debug(response)
                if response.status_code == 404:
                    f_url2 = f_url + '_p0.png'
                    response = requests.get(f_url2, verify=False, headers=headers, cookies=cookie)
                    if response.status_code == 404:
                        print("这是张动态图片无法下载,可以前往该url查看:" + "https://www.pixiv.net/artworks/" + pic_name + "\n")
                        return True
                    else:
                        with open(path + '\\' + str(pic_name) + '.png', 'wb') as f:
                            f.write(response.content)
                            print("第" + str(b) + "张图片已下载成功,图片的编号：%s\n图片url：%s\n" % (pic_name, f_url2))
                            return True
                else:
                    with open(path + '\\' + str(pic_name) + '.jpg', 'wb') as f:
                        f.write(response.content)
                        print("第" + str(b) + "张图片已下载成功,图片的编号：%s\n图片url：%s\n" % (pic_name, f_url1))
                        return True
            except:
                print("图片下载失败进行重试")
                x += 1
                if x == 10:
                    print("网络错误")
                    return False

    @staticmethod
    def edge_running(numb, url_base, data):
        the_urls = []
        n = 0
        while True:
            try:
                time.sleep(2)
                the_url = url_base + '/ranking.php?mode=daily&date=' + str(data) + '&?p=' + str(numb) + '&format=json'
                res = requests.get(the_url, verify=False).text
                # 当用driver获取到的是整个的html,是字符串格式----不对etree对象有用
                info = json.loads(res)
                for m in range(50):
                    try:
                        illust_id = info['contents'][m]['url']
                        the_urls.append(illust_id)
                    except IndexError:
                        print('爬取已完成')
                return the_urls
            except:
                print("请求失败正在进行重试")
                n += 1
                if n == 20:
                    print("网络失败")
                    return the_urls

    def download(self, data):
        a = 0
        for num in range(1, 11):
            urls = self.edge_running(num, self.base_url, data)
            if not urls:
                return False
            for i in urls:
                fragment = i[40:73]
                url = 'https://i.pximg.net/img-original' + fragment
                a += 1
                r = random.randint(1, 3)
                time.sleep(r)
                if self.get_DL(url, self.cookies, self.agent, self.filepath, a):
                    time.sleep(0.5)
                else:
                    return False
            time.sleep(3)
        return True
