from pac.pixLogin import PixivLogin
import json
import random
import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DownloadRun:
    def __init__(self, filepath, execute_path, username, password):
        self.filepath = filepath
        self.base_url = 'https://www.pixiv.net'
        self.userName = username
        self.pwd = password
        self.exePath = execute_path

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
                if response.status_code == 404:
                    f_url2 = f_url + '_p0.png'
                    response = requests.get(f_url2, verify=False, headers=headers, cookies=cookie)
                    if response.status_code == 404:
                        print("这是张动态图片无法下载,可以前往该url查看:" + "https://www.pixiv.net/artworks/" + pic_name)
                        break
                    else:
                        with open(path + '/' + str(pic_name) + '.png', 'wb') as f:
                            f.write(response.content)
                            print("第" + str(b) + "张图片已下载成功,图片的编号：", pic_name)
                            print("图片url：", f_url2)
                        break
                else:
                    with open(path + '/' + str(pic_name) + '.jpg', 'wb') as f:
                        f.write(response.content)
                        print("第" + str(b) + "张图片已下载成功，图片的编号：", pic_name)
                        print("图片url：", f_url1)
                    break
            except:
                print("下载失败进行重试")
                x += 1
                if x == 10:
                    break
        if x == 10:
            print("网络错误")

    @staticmethod
    def edge_running(numb, url_base, data):
        n = 0
        while True:
            try:
                time.sleep(2)
                the_url = url_base + '/ranking.php?mode=daily&date=' + str(data) + '&?p=' + str(numb) + '&format=json'
                res = requests.get(the_url, verify=False).text
                # 当用driver获取到的是整个的html,是字符串格式----不对etree对象有用
                info = json.loads(res)
                the_urls = []
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
                    break
        if n == 20:
            print("网络失败")

    def download(self, data):
        # 调用封装好的登录类
        login = PixivLogin(
            "https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=zh&source=pc&view_type=page",
            self.exePath
        )
        # 你的账号和密码
        login.handle_login(self.userName, self.pwd)
        cookies = login.get_cookie()
        agent = login.get_agent()
        print("cookie:", cookies)
        print("useragent:", agent)
        login.quit()
        # 下载排行榜的日期
        a = 0
        for num in range(1, 11):
            urls = self.edge_running(num, self.base_url, data)
            for i in urls:
                fragment = i[40:73]
                url = 'https://i.pximg.net/img-original' + fragment
                a += 1
                r = random.randint(1, 3)
                time.sleep(r)
                self.get_DL(url, cookies, agent, self.filepath, a)
                time.sleep(0.5)
            time.sleep(3)
