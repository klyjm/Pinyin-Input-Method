import numpy as np
f = open("D:\\拼音输入法作业\\拼音汉字表.txt")
lines = f.readlines()
f.close()
f = open("D:\\拼音输入法作业\\拼音汉字表.txt")
letters = f.read()
letters = letters.split()
f.close()
count = len(letters)-len(lines)
lettertype = np.dtype([('letter', 'U1', 1), ('pinyin', 'U6', 1), ('count', 'i', 1), ('lettercount', 'i', \
                                                                                     count), \
                       ('p', 'f', count)])
#lettertype = np.dtype({'names': ['letter', 'pinyin', 'count', 'pcount', 'p'], 'formats': ['U1', 'U6', 'i', 'i', 'f'], 'itemsize': []})
types = np.array([('', '', 0, np.zeros(count, dtype=np.int), np.zeros(count, dtype=np.float))]*count, dtype=lettertype)
j = 0
for line in lines:
    line = line.split()
    for i in range(1, len(line)):
        types[j+i-1]['letter'] = line[i]
        types[j+i-1]['pinyin'] = line[0]
    j = j+i
f = open("D:\\拼音输入法作业\\sina_news_gbk\\2016-02.txt")
lines = f.readlines()
print(len(lines))
f.close()
f = open("D:\\拼音输入法作业\\sina_news_gbk\\2016-04.txt")
lines.extend(f.readlines())
print(len(lines))
#for line in lines: