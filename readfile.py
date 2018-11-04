import numpy as np


def init():
    f = open("D:\\拼音输入法作业\\拼音汉字表.txt")
    lines = f.readlines()
    f.close()
    f = open("D:\\拼音输入法作业\\拼音汉字表.txt")
    letters = f.read()
    letters = letters.split()
    f.close()
    count = len(letters)-len(lines)
    lettertype = np.dtype([('letter', 'U1', 1), ('pinyin', 'U6', 1), ('count', 'i', 1), ('lettercount', 'O'), \
                       ('p', 'O')])
#lettertype = np.dtype({'names': ['letter', 'pinyin', 'count', 'pcount', 'p'], 'formats': ['U1', 'U6', 'i', 'i', 'f'], 'itemsize': []})
    types = np.array([('', '', 0, [0]*count, [0.]*count)]*(count+1), dtype=lettertype)
    j = 0
    for line in lines:
        line = line.replace('\n', '')
        line = line.split()
        for i in range(1, len(line)):
            types[j+i-1]['letter'] = line[i]
            types[j+i-1]['pinyin'] = line[0]
        j = j+i
    f = open('init', 'w')
    f.write('True')
    f.write('\n')
    f.write(str(count))
    f.close()
    return types


def practice(filename, types):
    f = open(filename)
    lines = f.readlines()
    f.close()
    for line in lines:
        j = [0]
        for i in range(len(line)):
            k = np.argwhere(types['letter'] == line[i])
            if len(k) > 0:
                for l in range(len(k)):
                    m = k[l][0]
                    types[m]['count'] += 1
                    if isinstance(j, int):
                        types[j]['lettercount'][m] += 1
                    else:
                        for n in range(len(j)):
                            types[j[n]]['lettercount'][m] += 1
                j = k[:][0].tolist()
            else:
                j = [0]
    for i in range(len(types['letter'])):
        if types[i]['count'] == 0:
            types[i]['p'][j] = 0
        else:
            for j in range(len(types[i]['lettercount'])):
                types[i]['p'][j] = types[i]['lettercount'][j]/types[i]['count']
    f = open('typefile', 'w')
    for i in range(len(types['letter'])):
        f.write(types[i]['letter'])
        f.write('\n')
        f.write(types[i]['pinyin'])
        f.write('\n')
        f.write(str(types[i]['count']))
        f.write('\n')
        for j in range(len(types[i]['lettercount'])):
            f.write(str(types[i]['lettercount'][j]))
            f.write('\n')
        for j in range(len(types[i]['p'])):
            f.write(str(types[i]['p'][j]))
            f.write('\n')
    f.close()
    return types


def process(line, types):
    string = ['']*len(line)
    pline = [0]*len(line)
    for i in range(len(line)):
        index = np.argwhere(types['pinyin'] == line[i])
        index = index[:][0].tolist()
        if isinstance(index, int):
            pline[i] = 0.
        else:
            pline[i] += [0.]*len(index)
    return string

f = open('init','w+')
initflag = f.readline().strip('\n')
f.close()
if initflag != 'True':
    types = init()
else:
    f = open('init')
    count = f.readline()
    count = int(f.readline())
    lettertype = np.dtype([('letter', 'U1', 1), ('pinyin', 'U6', 1), ('count', 'i', 1), ('lettercount', 'O'), \
                           ('p', 'O')])
    types = np.array([('', '', 0, [0] * count, [0.] * count)] * (count + 1), dtype=lettertype)
    f = open('typefile')
    for i in range(len(types['letter'])):
        types[i]['letter'] = f.readline().strip('\n')
        types[i]['pinyin'] = f.readline().strip('\n')
        types[i]['count'] = int(f.readline().strip('\n'))
        for j in range(len(types[i]['lettercount'])):
            types[i]['lettercount'][j] = int(f.readline().strip('\n'))
        for j in range(len(types[i]['p'])):
            types[i]['p'][j] = float(f.readline().strip('\n'))
    f.close()
inputstr = input('请输入命令：\n')
while len(inputstr.strip()) > 0:
    inputstr = inputstr.strip().split()
    if inputstr[0] == 'exit':
        exit()
    if inputstr[0] == 'practice':
        filename = inputstr[1]
        types = practice(filename, types)
    if inputstr[0] == 'pinyin':
        inputfilename = inputstr[1]
        outputfilename = inputstr[2]
        f = open(inputfilename)
        lines = f.readlines()
        f.close()
        string = ['']*len(lines);
        i = 0
        for line in lines:
            line = line.strip('\n').split()
            string[i] = process(line, types)+'\n'
            i += 1
        f = open(outputfilename, 'w')
        f.writelines(string)
        f.close()
    inputstr = input('请输入命令：\n')
