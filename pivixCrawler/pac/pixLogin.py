import time

import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options


class PixivLogin:
    def __init__(self, url, path):
        """
        对象初始化
        :param url: 首页地址
        """
        self.url = url
        self.browser = self.start_browser(path)

    @staticmethod
    def start_browser(path):
        op = Options()
        op.add_experimental_option("excludeSwitches", ["enable-automation"])
        op.page_load_strategy = 'eager'
        op.add_argument('--start-maximized')
        return webdriver.Edge(executable_path=path, options=op)

    @staticmethod
    def cookie_handle(cookies: list):
        """
        cookies 转化为字典函数
        :param cookies: selenium获取的cookies
        """
        dic = {}
        for i in cookies:
            dic[i["name"]] = i["value"]
            print("正在处理cookie：", len(dic))
        return dic

    def start_url(self):
        self.browser.get(self.url)

    def get_cookie(self):
        """
        使用requests对网址发送请求,并将请求结果存储
        存储cookies
        """
        cookie = self.cookie_handle(self.browser.get_cookies())
        return cookie

    def get_agent(self):
        agent = self.browser.execute_script("return navigator.userAgent")
        return agent

    def handle_login(self, username, pwd):
        """
        首页登录处理方法
        :param username: 用户名
        :param pwd: 用户密码
        """

        n = 0
        while True:
            try:
                self.start_url()
                self.browser.find_element(By.XPATH,
                                          '//*[@id="app-mount-point"]/div/div[3]/div[1]/form/fieldset[1]/label/input').send_keys(
                    username)
                self.browser.find_element(By.XPATH,
                                          '//*[@id="app-mount-point"]/div/div[3]/div[1]/form/fieldset[2]/label/input').send_keys(
                    pwd + Keys.ENTER)
                time.sleep(5)
                self.browser.execute_script("window.stop()")
                if self.browser.get_cookies() != {}:
                    break
            except:
                self.start_url()
                n += 1
                if n == 5:
                    break
        if n == 5:
            print("请检查网络")

    def quit(self):
        # 关闭浏览器
        self.browser.quit()
