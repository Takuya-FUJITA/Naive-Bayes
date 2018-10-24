# -*- coding: utf-8 -*-
#参考文献
#http://moguranosenshi.hatenablog.com/entry/2014/02/28/%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%A7%E5%8D%98%E8%AA%9E%E3%82%AB%E3%82%A6%E3%83%B3%E3%83%88
#
import pandas as pd
import sys
import codecs
import MeCab
from collections import defaultdict

def trans_data(loadfile, outfile):
   #ツイートとラベルをロード
   fp = codecs.open(loadfile, "r", "utf-8")
   load = []
   for line in fp:
      line = line.rstrip()
      load.append(line)
   fp.close()

   #総文書数
   num = len(load)

   #単語を区切る
   train_data = []
   x = ''
   
   for line in load:
      words = line.lower().split()
      for wc in words[1:]:
         word, count = wc.split(':ango:')
         for i in range(int(count)):
            x = x + word + ' '
      train_data.append(x)
      x = ''
   
   #ファイルに出力
   fp = open(outfile, 'w')
   for i in range(num):
      fp.write('%s\n' % train_data[i])
   fp.close()


if __name__ == "__main__":
   # トレーニングデータを変換
   trans_data("news20", "news20.txt")
   # テストデータを変換
   trans_data("news20_t", "news20_t.txt")
