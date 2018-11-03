import numpy as np
f = open("D:\\拼音输入法作业\\拼音汉字表.txt")
lines = f.readlines()
f.close()
f = open("D:\\拼音输入法作业\\拼音汉字表.txt")
letters = f.read()
letters = letters.split()
f.close()
count = len(letters)-len(lines)
lettertype = np.dtype([('letter', 'U1', 1), ('pinyin', 'U6', 2), ('count', 'i', 1), ('lettercount', 'O'), \
                       ('p', 'O')])
#lettertype = np.dtype({'names': ['letter', 'pinyin', 'count', 'pcount', 'p'], 'formats': ['U1', 'U6', 'i', 'i', 'f'], 'itemsize': []})
types = np.array([('', ['']*2, 0, [0]*count, [0.]*count)]*(count+1), dtype=lettertype)
j = 0
for line in lines:
    line = line.split()
    for i in range(1, len(line)):
        types[j+i-1]['letter'] = line[i]
        types[j+i-1]['pinyin'] = line[0]
    j = j+i
f = open("D:\\拼音输入法作业\\sina_news_gbk\\2016-02.txt")
lines = f.readlines()
f.close()
f = open("D:\\拼音输入法作业\\sina_news_gbk\\2016-04.txt")
lines.extend(f.readlines())
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
            j = 0
