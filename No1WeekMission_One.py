# Author : 张桐
# Create Date: 2017-06-27
# instruction: 模拟登陆，登陆失败超过三次锁定,针对已有用户输入密码错误,隐藏密码输入功能在pycharm下运行有问题,通过命令终端调试无问题

import json
import getpass
count = 0
pwd = None
urn = None
L = []
fileDst = "F:\CTO_week_mission\OneWeek\source\loginError.txt"
while True:
    print("*******登陆*********")
    userName = input("用户名: ")
    print("是否显示密码? y / n")
    choice = input("输入 :")
    if choice == 'y' or choice == 'Y':
        password = input("密码: ")
    elif choice == 'n' or choice == 'N':
        password = getpass.getpass("密码: ")
    else:
        continue
    # 登陆验证
    # 从文件里面找到读取用户名,密码,个人记载的登陆次数,三个字段信息
    with open(fileDst, 'r', encoding='utf-8') as f:
        loadDict = json.load(f)    # JSON转换成DICT字典
        # print(loadDict)
        if loadDict.get(userName) is None:
            print("账户未注册!")
        else:
            # print(loadDict.get(userName))
            L = loadDict.get(userName)
            urn = userName
            pwd = L[0]    # 密码
            count = int(L[1])    # 登陆失败记录次数
            if count >= 3:
                print("您的账户已被锁定!")
                count = 0
            else:
                if urn == userName and password == pwd:
                    print("登陆成功")
                    # 将当前账户登陆失败次数清零写入文件记录
                    loadDict.get(userName)[1] = 0
                    # 将当前账户登陆失败次数清零写入文件记录
                    with open(fileDst, 'w', encoding='utf-8') as f:
                        json.dump(loadDict, f)
                        f.flush()    # 将缓存数据实时刷入文件
                    break
                else:
                    if password != pwd:
                        if urn == userName:
                            print("用户名或者密码错误!")
                            count += 1
                            # 将当前账户登陆失败次数写入文件JSON记录
                            loadDict.get(userName)[1] = count
                            with open(fileDst, 'w', encoding='utf-8') as f:
                                json.dump(loadDict, f)
                                f.flush()