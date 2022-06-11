import json
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

    @staticmethod
    def get_DL(self, f_url, b):
        pic_name = f_url[-8:]
        f_url1 = f_url + '_p0.jpg'
        userAgent = UserAgent(verify_ssl=False).random
        headers = {
            'user-agent': userAgent,
            'Referer': 'https://www.pixiv.net/'
        }

        x = 0
        while True:
            try:
                response = requests.get(f_url1, verify=False, headers=headers, cookies=self.cookies)
                if response.status_code == 404:
                    f_url2 = f_url + '_p0.png'
                    response = requests.get(f_url2, verify=False, headers=headers, cookies=self.cookies)
                    if response.status_code == 404:
                        print("这是张动态图片无法下载,可以前往该url查看:" + "https://www.pixiv.net/artworks/" + pic_name + "\n")
                        return True
                    else:
                        with open(self.filepath + '\\' + str(pic_name) + '.png', 'wb') as f:
                            f.write(response.content)
                            print("第" + str(b) + "张图片已下载成功,图片的编号：%s\n图片url：%s\n" % (pic_name, f_url2))
                            return True
                else:
                    with open(self.filepath + '\\' + str(pic_name) + '.jpg', 'wb') as f:
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
    def edge_running(self, numb, data, R_18):
        userAgent = UserAgent(verify_ssl=False).random
        headers = {
            'user-agent': userAgent,
            'Referer': 'https://www.pixiv.net/'
        }

        the_urls = []
        n = 0
        while True:
            try:
                time.sleep(2)
                if R_18:
                    the_url = self.base_url + '/ranking.php?mode=daily_r18' + '&date=' + str(data) + '&p=' + str(
                        numb) + '&format=json'
                else:
                    the_url = self.base_url + '/ranking.php?mode=daily' + '&date=' + str(data) + '&p=' + str(
                        numb) + '&format=json'
                res = requests.get(the_url, verify=False, headers=headers, cookies=self.cookies).text
                # 处理获取的json
                info = json.loads(res)
                for m in range(50):
                    try:
                        url = info['contents'][m]['url']
                        the_urls.append(url)
                    except IndexError:
                        print('当前页面url获取完毕')
                        return the_urls
                return the_urls
            except:
                print("请求失败正在进行重试")
                n += 1
                if n == 20:
                    print("网络失败")
                    return the_urls

    def download(self, data, R18):
        a = 0
        for num in range(1, 20):
            urls = self.edge_running(self, num, data, R18)
            if not urls:
                return False
            for i in urls:
                fragment = i[40:73]
                url = 'https://i.pximg.net/img-original' + fragment
                a += 1
                r = random.randint(1, 3)
                time.sleep(r)
                if self.get_DL(self, url, a):
                    time.sleep(0.5)
                else:
                    return False
            time.sleep(3)
        return True
