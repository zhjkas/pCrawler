import inspect
import json
import logging
import os
from pac.picDLRun import DownloadRun


# 运行前的参数设置或读取
class Interaction:
    def __init__(self):
        # 获取运行参数所在文件夹
        self.current_file_name = inspect.getfile(inspect.currentframe())[:-19]
        self.userLog = self.current_file_name + r'\log\userLog\userLogin.json'
        print(self.current_file_name)
        print(self.userLog)
        # 如果没有就生成一个再读取，如果有就直接读取以前的运行参数
        if os.path.isfile(self.userLog):
            with open(self.userLog, "r", encoding="utf-8") as f_r:
                self.user_log = json.load(f_r)
        else:
            self.first_load(self)
            with open(self.userLog, "r", encoding="utf-8") as f_r:
                self.user_log = json.load(f_r)
        print(self.user_log)
        # 加载本地的用户参数
        self.filepath = self.user_log['filepath']
        self.executable_path = self.user_log['executable_path']
        self.programLog = self.user_log['programLog']
        self.username = self.user_log['username1']
        self.password = self.user_log['password1']
        # username的数量+1
        self.num = (len(self.user_log) - 2) // 2

    # 程序第一次运行初始化用户参数
    @staticmethod
    def first_load(self):
        # 前面4个存储运行时所需要的地址，默认为项目文件夹下
        dic0 = {'filepath': self.current_file_name + r'\pixiv排行榜',
                'executable_path': self.current_file_name + r'\edgedriver\msedgedriver.exe',
                'userLog': self.current_file_name + r'\log\userLog',
                'programLog': self.current_file_name + r'\log\programLog',
                'username1': '',
                'password1': ''
                }
        self.userLogSave(self, dic0)

    # 把字典转成json保存在本地
    @staticmethod
    def userLogSave(self, dic):
        # dump 将数据转换成字符串, sort:顺序打印 indent：打印格式的缩进 separators：‘元素之间用逗号隔开’,‘key和内容之间’ 用冒号隔开
        # Python引入了with语句来自动调用close()方法
        with open(self.userLog, "w", encoding="utf-8") as f_w:
            f_w.write(json.dumps(dic, sort_keys=False, indent=4, separators=(',', ': ')))

    @staticmethod
    def userLogin(self):
        # 判断某一对象(需提供绝对路径)是否为文件
        print("是否登录账号（建议登录）：Y/N ")
        input1 = input()
        if input1 == 'Y' or input1 == 'y':
            if self.username != '':
                if self.num > 2:
                    print("检查到多账号，是否进行多账户选择\n：Y/N")
                    input0 = input()
                    if input0 == 'Y' or input0 == 'y':
                        for i in range(1, self.num):
                            print(self.user_log["username" + str(i)])
                        print("想用那个账号进行登录(输入1，2，3···)")
                        print(self.user_log)
                        input1 = input()
                        self.username = self.user_log['username' + input1]
                        self.password = self.user_log['password' + input1]
            else:
                print("检查为首次登录，请输入账号和密码")
                print("用户名：")
                username = input()
                print("密码：")
                password = input()
                self.user_log['username1'] = username
                self.user_log['password1'] = password
                self.username = username
                self.password = password
                self.userLogSave(self, self.user_log)
        else:
            print("小心ip被ban哦！")
            self.username = ''
            self.password = ''

    @staticmethod
    def set(self, m):
        if m == '1':
            print("请更改图片保存位置：")
            a = input()
            self.user_log['filepath'] = a
            self.filepath = a
        if m == '2':
            print("请更改edge浏览器驱动位置：")
            a = input()
            self.user_log['executable_path'] = a
            self.executable_path = a
        if m == '3':
            print("用户名")
            a = input()
            self.user_log['username' + str(self.num)] = a
            print("密码")
            b = input()
            self.user_log['password' + str(self.num)] = b
            print("是否用该账号登录：Y/N")
            input1 = input()
            if input1 == 'Y' or input1 == 'y':
                self.username = a
                self.password = b
        self.userLogSave(self, self.user_log)
    # 程序运行
    def running(self):
        self.userLogin(self)
        print("是否更改设置：Y/N")
        x = input()
        if x == 'Y' or x == 'y':
            print("*****************")
            print("更改图片保存位置请扣1\n更改浏览器驱动位置请扣2\n添加用户请扣3")
            print("*****************")
            m = input()
            self.set(self, m)
        # 下载那一天的排行榜
        print("下载那一天的排行榜 eg:20220603")
        data = input()  # 20220601
        try:
            logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                                level=logging.DEBUG,
                                filename=self.programLog + r'\running.log',
                                filemode='a')
            print(self.executable_path)
            running = DownloadRun(self.filepath, self.executable_path, self.username, self.password)
            running.download(data)
        except:
            print("程序出错了！")
            print("按任意键退出")
            input()