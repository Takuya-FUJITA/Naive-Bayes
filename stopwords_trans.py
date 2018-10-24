# -*- coding: utf-8 -*-
#参考文献
#http://moguranosenshi.hatenablog.com/entry/2014/02/28/%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%A7%E5%8D%98%E8%AA%9E%E3%82%AB%E3%82%A6%E3%83%B3%E3%83%88
#
import pandas as pd
import sys
import codecs
import MeCab
from collections import defaultdict

def trans_data(tweetfile, outfile):
   # カテゴリをロード
   category = []
   fp = open("train.map")
   for line in fp:
      line = line.rstrip()
      category.append(line.split()[0])
   fp.close()
   #print(category)

   #ストップワードをロード
   stopwords = []
   fp = open('particle.txt')
   for line in fp:
      line = line.rstrip()
      stopwords.append(line)
   fp.close()
   
   #ツイートとラベルをロード
   fp = codecs.open(tweetfile, "r", "utf-8")
   tweet = []
   label = []
   for line in fp:
      line = line.rstrip()
      line = line.split(",a,n,g,o,")   #本文中に絶対ない文字列を設定
      tweet.append(line[0])
      label.append(line[1])
   fp.close()
   #print(label)

   #データのラベルを扱うリスト
   train_label = []
   for line in label:
      if line == '1':
         train_label.append(category[0])
      elif line == '2':
         train_label.append(category[1])
   #print(train_label)
   
   #総文書数
   num = len(label)
   
   #変換
   train_data = []
   for i in range(num):
      train_data.append([])

   #mecabで分かち書きになるように単語を区切る
   n = 0
   for line in tweet:
      word2freq = defaultdict(int)
      mecab = MeCab.Tagger("-Owakati")
      words = mecab.parse(line).split()
      for word in words:
         word2freq[word] += 1
      #print(word2freq)

      #「単語：頻度」をそれぞれリストに追加
      key_list = []
      value_list = []
      for word, freq in sorted(word2freq.items(), key=lambda x: x[1], reverse=True):
         key_list.append(word)
         value_list.append(freq)
      #print(key_list)
      #print(value_list)

      #最終的なデータの生成
      for m in range(len(key_list)):
         if not key_list[m] in stopwords: #助詞を除く
            train_data[n].append('%s:ango:%d' % (key_list[m], value_list[m]))
      n += 1
      #print(train_data)

      #ファイルに出力
      fp = open(outfile, 'w')
      for i in range(num):
         fp.write('%s %s\n' % (train_label[i], ' '.join(train_data[i])))
      fp.close()

if __name__ == "__main__":
   # 訓練データを変換
   trans_data("train.csv", "news20")
   # テストデータを変換
   trans_data("test.csv", "news20.t")
