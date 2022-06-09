import logging

dic0 = {'filepath': 'pixiv排行榜',
        'executable_path': '/log/userLog',
        'userLog': '/log/userLog',
        'programLog': '/log/programLog',
        'username1': '',
        'password1': '',
        'username2': '',
        'password2': '',
        'username3': '',
        'password3': '',
        'username4': '',
        'password4': '',
        'username5': '',
        'password5': '',
        }
print(len(dic0))
print(dic0)
dic0['username' + '1'] = '1'
dic0['password' + '1'] = '1'
print((len(dic0) - 2) // 2 - 1)
for i in range(1, (len(dic0) - 2) // 2):
    print("username" + str(i) + ":", dic0["username" + str(i)])
n = 3
if n > 2:
    print("hello\nwww\n")
