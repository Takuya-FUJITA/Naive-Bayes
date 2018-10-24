# -*- coding: utf-8 -*-
#参考文献
#http://moguranosenshi.hatenablog.com/entry/2014/02/28/%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%A7%E5%8D%98%E8%AA%9E%E3%82%AB%E3%82%A6%E3%83%B3%E3%83%88
#
"""
データは70と72行目で変える
22行目はデータによって，トレーニングとテストを変えないといけない
"""
import pandas as pd
import sys
import codecs
import treetaggerwrapper
from collections import defaultdict

def trans_data(loadfile, outfile):
   #文書とラベルをロード
   fp = codecs.open(loadfile, "r", "utf-8")
   load = []
   for line in fp:
      line = line.rstrip()
      load.append(line)
   fp.close()
   fp = codecs.open("news20.t", "r", "utf-8")  #"news20" or "news20.t"
   doc1 = []
   for line in fp:
      line = line.rstrip()
      doc1.append(line.split()[0])
   fp.close()
   fp = codecs.open("train.map", "r", "utf-8")
   doc2 = []
   for line in fp:
      line = line.rstrip()
      doc2.append(line)
   fp.close()

   #総文書数
   num = len(load)

   #単語を区切る
   train_data = []
   x = ''
   #noun = ["NN","NNS","NP","NPS"]
   noun = ["NN","NNS"]
   tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='/usr/local/src/tree-tagger')

   i=0
   for line in load:
      tags = tagger.TagText(line)
      for tag in tags:
         tag1, tag2, tag3 = tag.split('\t')
         if tag2 in noun:
            x = x + tag1.lower() + ' '
      for j in range(len(doc2)):
         if doc1[i] in doc2[j]:
            x = x[:-1] + ",," + doc2[j].split()[1]
      train_data.append(x)
      x = ''
      i += 1

   #ファイルに出力
   fp = open(outfile, 'w')
   for i in range(num):
      fp.write('%s\n' % train_data[i])
   fp.close()

"""
22行目はデータによって，トレーニングとテストを変えないといけない
"""
if __name__ == "__main__":
   # トレーニングデータを変換
   #trans_data("news20.txt", "news20_noun.txt")
   # テストデータを変換
   trans_data("news20_t.txt", "news20_t_noun.txt")
