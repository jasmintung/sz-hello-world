import os
import json
import getpass

balance = 0    # 账户余额
consumerBarcode = 0    # 单号
purcharsedgoods = []
goods = []

dictAccount = {}
accountInfo = {}
count = 0
choiceNum = 0
userName = None
pwd = None
urn = None
L = []
loginStatue = False
retryGoodNumber = False
userfileDst = "F:\pycharmProj\shopcar\\users.txt"
recordFileDst = "F:\pycharmProj\shopcar\\buyRecords.txt"
goodsFileDst = "F:\pycharmProj\shopcar\goods.txt"
accountFileDst = "F:\pycharmProj\shopcar\\accountManager.txt"
while True:
    print("**********欢迎**********")
    loginRole = input("普通用户请输入: 1\n管理员请输入: 2\n退出请输入: 0\n--->")
    if loginRole.isdigit():
        loginRole = int(loginRole)    # 必须要类型转换,输入的默认类型是字符串
        if loginRole == 1:
            print("欢迎光临")
            # import loginCheck
            # loginCheck()            # 后期这里传入文件的地址,身份验证
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
                with open(userfileDst, 'r', encoding='utf-8') as f:
                    loadDict = json.load(f)  # JSON转换成DICT字典
                    # print(loadDict)
                    if loadDict.get(userName) is None:
                        print("账户未注册!")
                    else:
                        # print(loadDict.get(userName))
                        L = loadDict.get(userName)
                        urn = userName
                        pwd = L[0]  # 密码
                        count = int(L[1])  # 登陆失败记录次数
                        if count >= 3:
                            print("您的账户已被锁定!")
                            count = 0
                            loginStatue = False
                        else:
                            if urn == userName and password == pwd:
                                print("登陆成功")
                                # 将当前账户登陆失败次数清零写入文件记录
                                loadDict.get(userName)[1] = 0
                                # 将当前账户登陆失败次数清零写入文件记录
                                with open(userfileDst, 'w', encoding='utf-8') as f:
                                    json.dump(loadDict, f)
                                    f.flush()  # 将缓存数据实时刷入文件
                                loginStatue = True
                                break
                            else:
                                if password != pwd:
                                    if urn == userName:
                                        print("用户名或者密码错误!")
                                        count += 1
                                        # 将当前账户登陆失败次数写入文件JSON记录
                                        loadDict.get(userName)[1] = count
                                        with open(userfileDst, 'w', encoding='utf-8') as f:
                                            json.dump(loadDict, f)
                                            f.flush()
            if loginStatue is True:
                isUpdateAccount = False
                with open(accountFileDst, 'r', encoding="utf-8") as af:
                    fileLength = os.path.getsize(accountFileDst)
                    if fileLength > 0:
                        accountInfo = json.load(af)
                        if userName not in accountInfo:
                            print("您的账户还没有存钱.")
                            deposit = int(input("请输入存放的金额: "))
                            account = {"余额": deposit}
                            accountInfo[userName] = account
                            balance = deposit
                            isUpdateAccount = True
                        else:
                            print(accountInfo)
                            print("您当前的余额是: ")
                            balance = accountInfo.get(userName).get("余额")
                            print(balance)
                            print("可以购买的商品:")  # 列出商品信息
                    else:
                        print("您的账户还没有存钱.")
                        deposit = int(input("请输入存放的金额: "))
                        account = {"余额": deposit}
                        accountInfo[userName] = account
                        balance = deposit
                        isUpdateAccount = True
                if isUpdateAccount is True:
                    with open(accountFileDst, 'w+', encoding="utf-8") as wf:
                        wf.writelines(json.dumps(accountInfo, ensure_ascii=False))  # 把字典转为json格式存入文件
                    isUpdateAccount = False
                with open(goodsFileDst, 'r', encoding='utf-8') as gf:
                    goods = json.load(gf)
                while True:
                    for i in range(len(goods)):
                        if i % 2 == 0:
                            j = i
                            print("编号: ", goods[i])
                            print("%s:单价 %f 库存 %d" % (goods[j+1][0], goods[j+1][1],goods[j+1][2]))
                    print("请选择要购买的商品,根据编号选择！")
                    choiceNo = input("请按编号选择,退出请按'Q',返回登录请按'B'")
                    if choiceNo == 'Q':
                        # 外围循环也要退出
                        print("欢迎再次光临!")
                        break
                    elif choiceNo == 'B':
                        break
                    else:
                        if choiceNo.isdigit():
                            choiceNo = int(choiceNo)
                            for j in range(len(goods)):
                                if j % 2 == 0:
                                    if choiceNo == goods[j]:
                                        while True:
                                            print("请输入购买数量,否则退出(Q)")
                                            choiceNum = input()
                                            if choiceNum.isdigit():
                                                retryGoodNumber = True
                                                print("比较", choiceNum, goods[j + 1][2])
                                                if int(choiceNum) == 0:
                                                    print("购买数量不能为0!")
                                                else:
                                                    if (int(choiceNum) > int(goods[j + 1][2])) or (int(goods[j + 1][2]) == 0):
                                                        print("库存不够!")
                                                        print("继续输入:是,选择其它商品输入:否")    # 否的话退出只上一层while循环
                                                        quitBuy = input("请输入: ")
                                                        if quitBuy == '是':
                                                            continue
                                                        elif quitBuy == '否':
                                                            retryGoodNumber = False
                                                            break
                                                    else:
                                                        retryGoodNumber = True
                                                        break
                                            else:
                                                if choiceNum == 'Q':
                                                    retryGoodNumber = False
                                                    break
                                                else:
                                                    print("非法输入!")
                                                    retryGoodNumber = False
                                        if retryGoodNumber is True:
                                            getNumber = 0    # 实际可购买的商品数量
                                            if len(purcharsedgoods) != 0:
                                                for k in range(len(purcharsedgoods)):
                                                    if k % 3 == 0:
                                                        if purcharsedgoods[k] == goods[j + 1][0]:
                                                            print("购物车已有相同的商品")
                                                            # 购物车里已经有相同的商品,只需要更新数量
                                                            for i in range(int(choiceNum)):
                                                                if balance >= goods[j + 1][1]:
                                                                    balance -= goods[j + 1][1]
                                                                else:
                                                                    print("您的余额不够了!")
                                                                    break
                                                                getNumber += 1
                                                            print("增加%d个" % getNumber)
                                                            purcharsedgoods[k + 2] += getNumber
                                                            goods[j + 1][2] -= getNumber
                                                            break
                                                    else:    # 购物车车里还没有这个商品哦
                                                        if k == len(purcharsedgoods) - 1:
                                                            purcharsedgoods.append(goods[j + 1][0])  # 商品名称
                                                            purcharsedgoods.append(goods[j + 1][1])  # 商品单价
                                                            print("购物车还无此商品")
                                                            for i in range(int(choiceNum)):
                                                                if balance >= goods[j + 1][1]:
                                                                    balance -= goods[j + 1][1]
                                                                else:
                                                                    print("您的余额不够!")
                                                                    break
                                                                getNumber += 1
                                                            print("增加%d个" % getNumber)
                                                            purcharsedgoods.append(getNumber)
                                                            goods[j + 1][2] -= getNumber
                                            else:    # 购物车还是空的
                                                print("购物车还是空的!")
                                                purcharsedgoods.append(goods[j + 1][0])  # 商品名称
                                                purcharsedgoods.append(goods[j + 1][1])  # 商品单价
                                                for i in range(int(choiceNum)):
                                                    if balance >= goods[j + 1][1]:
                                                        balance -= goods[j + 1][1]
                                                    else:
                                                        print("您的余额不够!")
                                                        break
                                                    getNumber += 1
                                                print("增加%d个" % getNumber)
                                                purcharsedgoods.append(getNumber)
                                                goods[j + 1][2] -= getNumber
                                    else:
                                        if retryGoodNumber is True:
                                            if j == len(goods) - 1:
                                                print("抱歉没有这个商品哦")
                    if retryGoodNumber is True:
                        print("是否继续选购？继续(Y),打印小票(P)")
                        print(len(purcharsedgoods))
                        continueChoice = input()
                        if continueChoice == "Y":
                            pass
                        elif continueChoice == 'P':
                            if len(purcharsedgoods) == 0:
                                print("您的购物车是空的!")
                                purcharsedgoods.clear()
                            else:
                                print("------------------------------")
                                print("购物总计:")
                                print("\t名称:\t\t单价*数量\t\t\t小计")
                                for m in range(len(purcharsedgoods)):
                                    n = 0
                                    if m % 3 == 0:
                                        n = m + 1
                                        print("\t\t%s\t\t" % (purcharsedgoods[m]), purcharsedgoods[n], end='')
                                        print("*", end='')
                                        print(purcharsedgoods[n+1], end='')
                                        print("\t\t\t\t\t\t", purcharsedgoods[n]*purcharsedgoods[n+1])
                                print("------------------------------")
                                print("您的余额是: %d RMB" % balance)
                                print("是否继续选购？继续(B),结算(C),放弃(Q)")
                                continueChoice = input()
                                if continueChoice == "B":
                                    pass
                                elif continueChoice == "C":
                                    recordDict = {}
                                    with open(recordFileDst, 'r', encoding='utf-8') as rcf:
                                        recordFileLen = os.path.getsize(recordFileDst)
                                        if recordFileLen > 0:
                                            recordDict = json.load(rcf)
                                    shopcarList = {}
                                    recordLoadDict = {}
                                    writeFileRecordDict = {}
                                    print("支付成功!")
                                    # 将本次交易记录写入文件
                                    codeId = (1980, )
                                    consumerBarcode += codeId[0] + 1
                                    shopcarList["消费时间"] = "20170987-14:59"
                                    for m in range(len(purcharsedgoods)):
                                        n = 0
                                        if m % 3 == 0:
                                            n = m + 1
                                            buyThings = [purcharsedgoods[n+1], purcharsedgoods[n]]
                                            shopcarList[purcharsedgoods[m]] = buyThings
                                    recordLoadDict[consumerBarcode] = shopcarList
                                    recordDict.update(recordLoadDict)
                                    writeFileRecordDict[userName] = recordDict
                                    print(writeFileRecordDict)
                                    with open(recordFileDst, 'w', encoding='utf-8') as wf, \
                                         open(goodsFileDst, 'w', encoding='utf-8') as gdf, \
                                         open(accountFileDst, 'w', encoding='utf-8') as acf:
                                        # 更新购买记录
                                        wf.write(json.dumps(writeFileRecordDict, ensure_ascii=False))
                                        wf.flush()
                                        # 更新商品库存
                                        gdf.write(json.dumps(goods, ensure_ascii=False))
                                        gdf.flush()
                                        # 更新个人资产
                                        accountInfo.get(userName)["余额"] = balance
                                        acf.write(json.dumps(accountInfo, ensure_ascii=False))
                                    print("欢迎再次光临!")
                                    purcharsedgoods.clear()
                                    break
                                elif continueChoice == "Q":
                                    print("欢迎再次光临!")
                                    purcharsedgoods.clear()
                                    break
                        else:
                            print("输入有误,退出！！")
        elif loginRole == 2:
            import loginCheck
            # loginCheck()  # 后期这里传入文件的地址,身份验证
            # print("请选择要做的操作:")
        elif loginRole == 0:
            print("您已退出.")
            break
        else:
            print("输入有误")
            continue
    else:
        print("输入不正确!")



