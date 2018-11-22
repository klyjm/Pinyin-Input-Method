import numpy as np
import math
import time


#初始化函数
def init():
    f = open("拼音汉字表.txt")
    lines = f.readlines()
    f.close()
    f = open("拼音汉字表.txt")
    letters = f.read()
    letters = letters.split()
    f.close()
    count = len(letters)-len(lines)
    lettertype = np.dtype([('letter', 'U1', 1), ('pinyin', 'U6', 1), ('count', 'i', 1)])
    # lettertype = np.dtype([('letter', 'U1', 1), ('pinyin', 'U6', 1), ('count', 'i', 1), ('lettercount', 'O'), \
    #                    ('p', 'O')])
    # types = np.array([('', '', 0, [0]*count, [0.]*count)]*(count+1), dtype=lettertype)
    types = np.array([('', '', 0)] * (count + 1), dtype=lettertype)
    # for i in range(count+1):
    #     types[i]['lettercount'] = [0]*count
    #     types[i]['p'] = [0.]*count
    global lettercount
    global p
    global allcount
    allcount = 0
    lettercount = [0] * (count + 1)
    p = [0.] * (count + 1)
    for i in range(count + 1):
        lettercount[i] = [0]*count
        p[i] = [0.]*count #字的二元模型下，为该字后面跟随任何一个字的概率
    j = 0
    for line in lines:
        line = line.replace('\n', '')
        line = line.split()
        for i in range(1, len(line)):
            types[j+i-1]['letter'] = line[i]
            types[j+i-1]['pinyin'] = line[0]
        j = j+i
    f = open('init', 'a+')
    f.seek(0, 0)
    initflag = f.readline().strip('\n')
    if initflag != 'True':
        f.close()
        f = open('init', 'w')
        f.write('True')
        f.write('\n')
        f.write(str(count))
        f.close()
    else:
        # f = open('typefile')
        # allline = f.readlines()
        # j = 0
        # for i in range(len(types['letter'])):
        #     types[i]['letter'] = allline[j].strip('\n')
        #     j += 1
        #     types[i]['pinyin'] = allline[j].strip('\n')
        #     j += 1
        #     types[i]['count'] = int(allline[j].strip('\n'))
        #     j += 1
        #     for k in range(len(types[i]['lettercount'])):
        #         types[i]['lettercount'][k] = int(allline[j].strip('\n'))
        #         j += 1
        #     for k in range(len(types[i]['p'])):
        #         types[i]['p'][k] = float(allline[j].strip('\n'))
        #         j += 1
        # f.close()
        # del allline
        f.close();
        print('reading data......')
        start = time.time()
        f = open('types')
        allline = f.readlines()
        print(str(time.time() - start))
        print('processing data......')
        j = 0
        start = time.time()
        for i in range(len(types['letter'])):
            types[i]['count'] = int(allline[j].strip('\n'))
            allcount += types[i]['count']
            j += 1
            for k in range(count):
                # types[i]['lettercount'][k] = int(allline[j].strip('\n'))
                lettercount[i][k] = int(allline[j].strip('\n'))
                j += 1
        f.close()
        del allline
        print(str(time.time() - start))
        start = time.time()
        # for i in range(len(types['letter'])):
        #     if types[i]['count'] != 0:
                # types[i]['p'] = list(map(lambda x, y:0.9 * x / types[i]['count'] + 0.1 * y / allcount, types[i]['lettercount'], types['count']))
                # p[i] = list(map(lambda x, y: 0.9 * x / types[i]['count'] + 0.1 * y / allcount, lettercount[i], types['count']))
                # for j in range(len(types[i]['lettercount'])):
                #     types[i]['p'][j] = 0.9 * types[i]['lettercount'][j] / types[i]['count'] + 0.1 * types[j]['count'] / allcount
        print(str(time.time() - start))
    return types


#训练函数
def practice(filename, types, state):
    global practicedflag
    global w3count
    f = open(filename)
    lines = f.readlines()
    f.close()
    print('practing......')
    global allcount
    global p
    global lettercount
    if state == 'w2':
        for line in lines:
            j = [7497]
            for i in range(len(line)):
                k = np.argwhere(types['letter'] == line[i])
                if len(k) > 0:
                    for l in range(len(k)):
                        m = k[l][0]
                        types[m]['count'] += 1
                        allcount +=1
                        if isinstance(j, int):
                            # types[j]['lettercount'][m] += 1
                            lettercount[j][m] += 1
                        else:
                            for n in range(len(j)):
                                # types[j[n]]['lettercount'][m] += 1
                                lettercount[j[n]][m] += 1
                    j = [7497] * len(k)
                    for l in range(len(k)):
                        j[l] = k[l][0]
                else:
                    j = [7497]
        for i in range(len(types['letter'])):
            if types[i]['count'] == 0:
                # types[i]['p'][j] = 0
                p[i][j] = 0
            else:
                # for j in range(len(types[i]['lettercount'])):
                for j in range(len(lettercount[i])):
                    # types[i]['p'][j] = 0.9 * types[i]['lettercount'][j]/types[i]['count'] + 0.1 * types[j]['count'] / allcount
                    p[i][j] = 0.9 * lettercount[i][j] / types[i]['count'] + 0.1 * types[j]['count'] / allcount
    elif state == 'w3':
        count = len(types)
        for i in range(count - 1):
            p[i] = [0.] * (count * count) #字的三元模型即以上时，存储前面是某两个字时出现本字的概率
            lettercount[i] = [0] * (count * count)
        for line in lines:
            i = [7497] * 2 #前两个字的下标
            for j in range(len(line)):
                k = np.argwhere(types['letter'] == line[j])
                if len(k) > 0:
                    m = [0] * len(k)
                    for l in range(len(k)):
                        m[l] = k[l][0]
                    for l in range(m):
                        types[m]['count'] += 1
                        allcount += 1
                        if isinstance(i[0], int) & isinstance(i[1], int):
                            # types[j]['lettercount'][m] += 1
                            lettercount[m][i[0] * count + i[1]] += 1
                        elif isinstance(i[0], int) & ~isinstance(i[1], int):
                            for n in range(len(i[1])):
                                lettercount[m][i[0] * count + i[1][n]] += 1
                        elif ~isinstance(i[0], int) & isinstance(i[1], int):
                            for n in range(len(i[0])):
                                lettercount[m][i[0][n] * count + i[1]] += 1
                        else:
                            for n in range(len(i[0])):
                                for o in range(len(i[1])):
                                # types[j[n]]['lettercount'][m] += 1
                                    lettercount[m][i[0][n] * count + i[1][o]] += 1
                    i[0] = i[1]
                    i[1] = m
                else:
                    i = [7497] * 2
        for i in range(len(types['letter'])):
            if types[i]['count'] == 0:
                # types[i]['p'][j] = 0
                p[i][j] = [0.] * (count * count)
            else:
                for j in range(len(types[i]['lettercount'])):
                    # types[i]['p'][j] = 0.9 * types[i]['lettercount'][j]/types[i]['count'] + 0.1 * types[j]['count'] / allcount
                    p[i][j] = 0.9 * lettercount[i][j] / types[i]['count'] + 0.1 * types[j]['count'] / allcount
        global w3practiced
        w3practiced = True
    check(types)
    practicedflag = True
    return types


#程序有问题时写的检查程序
def check(types):
    allcount = 0
    for i in range(len(types)):
        # for j in range(len(types[i]['p'])):
        for j in range(len(p[i])):
            # if math.isnan(types[i]['p'][j]):
            if math.isnan(p[i][j]):
                # types[i]['p'][j] = 0
                p[i][j] = 0
                print(types[i]['letter'])
            # if types[i]['p'][j] > 1:
            if p[i][j] > 1:
                print('error', str(i), str(j))
        allcount += types[i]['count']


#动态规划求全局最优解，穷举算成zz
def process(line, types, state):
    n1 = len(line)  #拼音串长度
    string = [''] * n1  #转换得到的汉字串
    if state == 'w2':
        countline = [0] * n1  #存储每个拼音对应的汉字的数量
        indexline = [0] * n1  #存储每个拼音对应的每个汉字在字表中的下标
        for i in range(n1):
            line[i] = line[i].lower()
            tempindex = np.argwhere(types['pinyin'] == line[i])
            n = len(tempindex)
            countline[i] = n
            indexline[i] = [0] * n
            for j in range(n):
                indexline[i][j] = tempindex[j][0]
        lastmaxp = [1.] * 1  #上一个拼音对应的每个汉字对应的最大概率值
        lastindex = [7496] * 1  #上一拼音对应的每个汉字在字表中的下标
        maxindex = [0] * n1  #存储使当前汉字达到最大概率的汉字在上一个拼音对应的字符串中下标
        for i in range(n1):
            maxindex[i] = [0] * countline[i]
            tempmaxp = [0.] * countline[i]  #存储当前拼音对应的每个汉字的最大概率
            if isinstance(lastmaxp, int):
                for j in range(countline[i]):
                    # tempmaxp[j] = lastmaxp * types[lastindex]['p'][indexline[i][j]]
                    tempmaxp[j] = lastmaxp * p[lastindex][indexline[i][j]]
                    maxindex[i][j] = 0
            else:
                for j in range(countline[i]):
                    tempmaxindex = 0  #存储是当前汉字达到最大概率的汉字在上一个拼音对应的字符串的下标
                    for k in range(len(lastmaxp)):
                        # if lastmaxp[k] * types[lastindex[k]]['p'][indexline[i][j]] > tempmaxp[j]:
                        #     tempmaxp[j] = lastmaxp[k] * types[lastindex[k]]['p'][indexline[i][j]]
                        if lastmaxp[k] *  p[lastindex[k]][indexline[i][j]] > tempmaxp[j]:
                            tempmaxp[j] = lastmaxp[k] *  p[lastindex[k]][indexline[i][j]]
                            tempmaxindex = k
                    maxindex[i][j] = tempmaxindex
            lastmaxp = tempmaxp
            lastindex = indexline[i]
        pointer = lastmaxp.index(max(lastmaxp))
    for i in range(n1-1, -1, -1):
        try:
            string[i] = types[indexline[i][pointer]]['letter']
        except IndexError:
            print(line)
            print(str(indexline[i]))
            print(str(pointer))
            string = ''
        else:
            pointer = maxindex[i][pointer]
    return string


#内容转储函数
def rewrite(types):
    # f = open('types','w+')
    # for i in range(len(types)):
    #     f.write(str(types[i]['count']))
    #     f.write('\n')
    #     for j in range(len(types[i]['lettercount'])):
    #         f.write(str(types[i]['lettercount'][j]))
    #         f.write('\n')
    # f.close()
    with open('newtypes', 'w+') as f:
        for i in range(len(types)):
            f.write(str(types[i]['count'])+'\n')
            # for j in range(len(types[i]['lettercount'])):
            #     f.write(str(types[i]['lettercount'][j])+'\n')
            # for j in range(len(types[i]['p'])):
            #     f.write(str(types[i]['p'][j])+'\n')
            for j in range(len(lettercount[i])):
                f.write(str(lettercount[i][j])+'\n')
            for j in range(len(p[i])):
                f.write(str(p[i][j])+'\n')


#测试函数
def desperate(filename, types, state):
    with open(filename) as f:
        i = 0
        result = ['']
        allcount = 0
        correctcount = 0
        fo = open('output.txt','w')
        for line in f:
            if i:
                line = list(line.strip('\n').split()[0])
                allcount += len(line)
                for j in range(len(line)):
                    if line[j] == result[j]:
                        correctcount += 1
                result = ''.join(result)
                fo.write(result)
                fo.write('\n')
                i = 0
            else:
                line = line.strip('\n').split()
                for j in range(len(line)):
                    if line[j] == 'xv':
                        line[j] = 'xu'
                    if line[j] == 'qv':
                        line[j] = 'qu'
                result = process(line, types, state)
                i += 1
        fo.close()
    print(str(correctcount/allcount))


#状态切换函数
def switch(state):
    if state == 'w3':
        f = open("D:\\拼音输入法作业\\拼音汉字表.txt")
        lines = f.readlines()
        f.close()
        f = open("D:\\拼音输入法作业\\拼音汉字表.txt")
        letters = f.read()
        letters = letters.split()
        f.close()
        count = len(letters) - len(lines)
        lettertype = np.dtype([('letter', 'U1', 1), ('pinyin', 'U6', 1)])
        types = np.array([('', '')] * (count + 1), dtype=lettertype)
        global w3count
        global lettercount
        global p
        global allcount
        w3count = [0] * ((count + 1) ** 2)
        f = open('w3', 'a+')
        f.seek(0, 0)
        w3flag = f.readline().strip('\n')
        f.close()
        if w3flag == 'True':
            with open('w3count') as f:
                i = 0
                for line in f:
                    w3count[i] = line.strip('\n')
                    i += 1
            with open('w3types') as f:
                i = 0
                for line in f:
                    lettercount[i] = line.strip('\n')
                    i += 1
            for i in range(len(p)):
                p[i] = list(map(lambda x, y: 0.9 * x / y + 0.1 * types[i]['count'] / allcount, lettercount[i], w3count))


def change(types, filename, state):
    global lettercount
    global p
    global allcount
    # for l in [0.1, 0.2, 0.3, 0.4, 0.5]:
    #     for i in range(len(types['letter'])):
    #         if types[i]['count'] != 0:
    #             # types[i]['p'] = list(map(lambda x, y:0.9 * x / types[i]['count'] + 0.1 * y / allcount, types[i]['lettercount'], types['count']))
    #             p[i] = list(map(lambda x, y: (1.0 - l) * x / types[i]['count'] + l * y / allcount, lettercount[i], types['count']))
    #     desperate(filename, types, state)
    for l in [0.08, 0.06, 0.04, 0.03, 0.02, 0.0]:
        for i in range(len(types['letter'])):
            if types[i]['count'] != 0:
                # types[i]['p'] = list(map(lambda x, y:0.9 * x / types[i]['count'] + 0.1 * y / allcount, types[i]['lettercount'], types['count']))
                p[i] = list(map(lambda x, y: (1.0 - l) * x / types[i]['count'] + l * y / allcount, lettercount[i], types['count']))
        desperate(filename, types, state)



# f = open('init','a+')
# f.seek(0,0)
# initflag = f.readline().strip('\n')
# f.close()
state = 'w2'
types = init()
practicedflag = False
w3practiced = False
# if initflag != 'True':
#     types = init()
# else:
#     print('reading data......')
#     f = open('init')
#     count = f.readline()
#     count = int(f.readline().strip('\n'))
#     f.close()
#     lettertype = np.dtype([('letter', 'U1', 1), ('pinyin', 'U6', 1), ('count', 'i', 1), ('lettercount', 'O'), \
#                            ('p', 'O')])
#     types = np.array([('', '', 0, [0] * count, [0.] * count)] * (count + 1), dtype=lettertype)
#     for i in range(count+1):
#         types[i]['lettercount'] = [0]*count
#         types[i]['p'] = [0.]*count
#     f = open('typefile')
#     allline = f.readlines()
#     j = 0
#     for i in range(len(types['letter'])):
#         types[i]['letter'] = allline[j].strip('\n')
#         j += 1
#         types[i]['pinyin'] = allline[j].strip('\n')
#         j += 1
#         types[i]['count'] = int(allline[j].strip('\n'))
#         j += 1
#         for k in range(len(types[i]['lettercount'])):
#             types[i]['lettercount'][k] = int(allline[j].strip('\n'))
#             j += 1
#         for k in range(len(types[i]['p'])):
#             types[i]['p'][k] = float(allline[j].strip('\n'))
#             j += 1
#     f.close()
#     del allline
inputstr = input('请输入命令：\n')
while len(inputstr.strip()) >= 0:
    inputstr = inputstr.strip().split()
    if inputstr[0] == 'exit':
        if practicedflag:
            f = open('types', 'w')
            print('writing data......')
            for i in range(len(types['letter'])):
                # f.write(types[i]['letter'])
                # f.write('\n')
                # f.write(types[i]['pinyin'])
                # f.write('\n')
                f.write(str(types[i]['count']))
                f.write('\n')
                for j in range(len(types[i]['lettercount'])):
                    f.write(str(types[i]['lettercount'][j]))
                    f.write('\n')
                # for j in range(len(types[i]['p'])):
                #     f.write(str(types[i]['p'][j]))
                #     f.write('\n')
            f.close()
        if w3practiced:
            f = open('w3', 'w')
            f.write('True')
            f.close()
            print('writing data......')
            f = open('w3count', 'w')
            for i in range(w3count):
                f.write(str(w3count[i]))
                f.write('\n')
            for i in range(len(lettercount)):
                f.write(str(lettercount[i]))
                f.write('\n')
            f.close()
        exit()
    elif inputstr[0] == 'help':
        print('switch  state              功能：切换状态  参数解释：state：选择字的二元模型输入：--w2，选择字的三元模型输入：--w3')
        print('practice filename          功能：训练模型  参数解释：filename：为语料集文件路径，文件类型为txt')
        print('desperate filename         功能：利用验证集给出模型准确率 参数解释：filename：为验证集文件路径，文件类型为txt')
        print('pinyin filename1 filename2 功能：将输入文件中的拼音字符串转换为汉字并写入到输入文件中 参数解释：filename1：输入文件路径，filename2：输出文件路径，文件类型均为txt')
    elif inputstr[0] == 'switch':
        if len(inputstr) < 2:
            print('缺少状态关键词（例如：--w2），非法输入！')
        else:
            if inputstr[1] == '--w2':
                state = 'w2'
                types = init()
            elif inputstr[1] == '--w3':
                state = 'w3'
                switch(state)
    elif inputstr[0] == 'practice':
        filename = inputstr[1]
        types = practice(filename, types, state)
    elif inputstr[0] == 'check':
        check(types)
    elif inputstr[0] == 'rewrite':
        rewrite(types)
    elif inputstr[0] == 'desperate':
        desperate(inputstr[1], types, state)
    elif inputstr[0] == 'pinyin':
        if len(inputstr) < 3:
            print('输入非法！')
        else:
            inputfilename = inputstr[1]
            outputfilename = inputstr[2]
            f = open(inputfilename)
            lines = f.readlines()
            f.close()
            string = ['']*len(lines)
            i = 0
            error = 0
            for line in lines:
                line = line.strip('\n').split()
                for j in range(len(line)):
                    if line[j] == 'xv':
                        line[j] = 'xu'
                    if line[j] == 'qv':
                        line[j] = 'qu'
                string[i] = ''.join(process(line, types, state))
                string[i] += '\n'
                i += 1
            f = open(outputfilename, 'w')
            f.writelines(string)
            f.close()
    elif inputstr[0] == 'change':
        change(types, inputstr[1], state)
    else:
        print('非法输入！请正确输入命令！')
    inputstr = input('请输入命令：\n')
