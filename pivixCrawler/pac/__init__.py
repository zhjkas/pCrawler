from pac.picDLRun import DownloadRun

if __name__ == '__main__':
    # 图片保存位置
    print("请输入保存图片位置：")
    filepath = input()  # r'D:\1code\pivixCrawler\图片保存'
    # edge浏览器驱动位置
    print("edge浏览器驱动位置：")
    executable_path = input()  # r'D:\1code\pivixCrawler\edgedriver\msedgedriver.exe'
    # 用户名
    print("用户名")
    username = input()  # ''
    # 密码
    print("密码")
    password = input()  # ''
    # 下载那一天的排行榜
    print("下载那一天的排行榜 eg:20220603")
    data = input()  # 20220601

    running = DownloadRun(filepath, executable_path, username, password)
    running.download(data)
