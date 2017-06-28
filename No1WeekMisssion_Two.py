# Author : 张桐
# Create Date: 2017-06-27
# instruction: 三级菜单,显示省（直辖市）市区

import json

fileDst = "F:\CTO_week_mission\OneWeek\source\cities.txt"
recycle = True
highRecycle = True
middleRecycle = True
lowRecycle = True
while recycle:
    print("退出使用请输入大些字母 : Q")
    with open(fileDst, 'r', encoding='utf-8') as f:
        loadList = json.load(f)                     # JSON转换为 字典DICT
        # print(loadList)
        while highRecycle:
            for i in range(len(loadList)):
                loadListCity = loadList[i].get('city')
                print("->%s" % (loadList[i].get('name')))  # 列出各个省名字
            print("请输入要查看的省直辖市的完整名称")
            province = input("输入: ")
            if province == 'Q':
                recycle = False
                middleRecycle = False
                lowRecycle = False
                break
            else:
                for j in range(len(loadList)):
                    if province == loadList[j].get('name'):    # 输入正确
                        loadListCity = loadList[j].get('city')    # 指向这个省
                        for k in range(len(loadListCity)):
                            print("-->", loadListCity[k].get('name'))  # 各个市
                        highRecycle = False
                        middleRecycle = True
                        break
                    else:
                        if j == len(loadList) - 1:
                            print("不存在!")    # 输入错误
                            break
        while middleRecycle:
            print("请输入要查看的市的完整名称,返回上一级请输入: back")
            choice = input("请输入: ")
            if choice != "back" and choice != 'Q':
                for m in range(len(loadListCity)):
                    if choice == loadListCity[m].get('name'):    # 输入正确
                        print("--->", loadListCity[m].get('area'))
                        middleRecycle = False
                        lowRecycle = True
                        break
                    else:
                        if m == len(loadListCity) - 1:
                            print("不存在!")    # 输入错误
                            break
            else:
                if choice == 'back':
                    highRecycle = True
                    lowRecycle = False
                    break
                elif choice == 'Q':
                    recycle = False
                    middleRecycle = False
                    lowRecycle = False
                    break
                else:
                    print("无效输入!")
                    break
        while lowRecycle:
            print("返回上一级请输入: back,回到顶级请输入: roll")
            endChoice = input("输入: ")
            if endChoice == 'back':
                highRecycle = False
                middleRecycle = True
                lowRecycle = False
                break
            elif endChoice == 'roll':
                highRecycle = True
                middleRecycle = False
                break
            elif endChoice == 'Q':
                recycle = False
                highRecycle = False
                middleRecycle = False
                lowRecycle = False
                break
            else:
                print("无效输入!")

