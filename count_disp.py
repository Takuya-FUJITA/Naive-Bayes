# -*- coding: utf-8 -*-

#参考文献
#http://qiita.com/Hi-king/items/1e3e9aaae4195e3542c8
import pandas as pd
import sys
import codecs
import MeCab
from collections import defaultdict

'''
#「単語：頻度」をそれぞれリストに追加
key_list = []
value_list = []
for word, freq in sorted(word2freq.items(), key=lambda x: x[1], reverse=True):
   key_list.append(word)
   value_list.append(freq)
'''

# カテゴリをロード
category = []
fp = open("train.map")
for line in fp:
   line = line.rstrip()
   category.append(line.split()[0])
fp.close()
#print(category)

j = 0
cat = []
doc = [[] for i in range(len(category))]   #配列の確保
fp = open('news20')
for data in fp:
   data = data.rstrip()
   data = data.split()
   cat.append(data[0])
   for i in range(len(category)):   #カテゴリー2
      if category[i] == cat[j]:
         for word in data[1:]:      #単語分まわる
            word = word.split(':ango:')
            for f in range(int(word[1])): #頻度分配列に同じ単語を加える
               doc[i].append(word[0])
   j += 1
#print(cat)
#print(doc)

#上位１０単語の表示
for i in range(len(doc)):
   print(category[i])
   j = 0
   word_count = defaultdict(int)
   for word in doc[i]:
      word_count[word] += 1
   for k, v  in sorted(word_count.items(), key=lambda x:x[1], reverse=True):
      if j < 10:
         #print(k+' ', end='')
         print(k+'/', end='')
      j += 1
   print()
   print()
