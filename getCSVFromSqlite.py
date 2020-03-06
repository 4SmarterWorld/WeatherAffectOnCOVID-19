# coding:utf-8
import sqlite3
import csv, codecs
from io import StringIO
'''
link:https://www.jb51.net/article/118587.htm
'''

def writerows(file, rows):
    for row in rows:
        line = ''
        for s in row:
            line = line + s + ','
        print(line)
        file.write(line)
        file.write('\n')

conn = sqlite3.connect('citylist.sqlite')
c = conn.cursor()
c.execute('select * from citylist')
with open("citylist.csv", "w+") as fp:
    writerows(fp,c)
