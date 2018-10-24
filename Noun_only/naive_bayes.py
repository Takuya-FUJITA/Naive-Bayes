#http://aidiary.hatenablog.com/entry/20100618/1276877116
#http://aidiary.hatenablog.com/entry/20100613/1276389337
#coding:utf-8
import codecs
import math
import sys
from collections import defaultdict
#from naivebayes import NaiveBayes

class NaiveBayes:
   """Multinomial Naive Bayes"""
   def __init__(self):
      self.categories = set()     # カテゴリの集合
      self.vocabularies = set()   # ボキャブラリの集合
      self.wordcount = {}         # wordcount[cat][word] カテゴリでの単語の出現回数
      self.catcount = {}          # catcount[cat] カテゴリの出現回数
      self.denominator = {}       # denominator[cat] P(word|cat)の分母の値
   def train(self, data):
      """ナイーブベイズ分類器の訓練"""
      # 文書集合からカテゴリを抽出して辞書を初期化
      for d in data:
         cat = d[0]
         self.categories.add(cat)
      for cat in self.categories:
         self.wordcount[cat] = defaultdict(int)
         self.catcount[cat] = 0
      # 文書集合からカテゴリと単語をカウント
      for d in data:
         cat, doc = d[0], d[1:]
         self.catcount[cat] += 1
         for wc in doc:
            word, count = wc.split(":")
            count = int(count)
            self.vocabularies.add(word)
            self.wordcount[cat][word] += count
      # 単語の条件付き確率の分母の値をあらかじめ一括計算しておく（高速化のため）
      for cat in self.categories:
         self.denominator[cat] = sum(self.wordcount[cat].values()) + len(self.vocabularies)
      
   def classify(self, doc):
      """事後確率の対数 log(P(cat|doc)) がもっとも大きなカテゴリを返す"""
      best = None
      max = -sys.maxsize#max = -sys.maxint
      for cat in self.catcount.keys():
         p = self.score(doc, cat)
         if p > max:
            max = p
            best = cat
      return best
      
   def wordProb(self, word, cat):
      """単語の条件付き確率 P(word|cat) を求める"""
      # ラプラススムージングを適用
      # wordcount[cat]はdefaultdict(int)なのでカテゴリに存在しなかった単語はデフォルトの0を返す
      # 分母はtrain()の最後で一括計算済み
      return float(self.wordcount[cat][word] + 1) / float(self.denominator[cat])

   def score(self, doc, cat):
      """文書が与えられたときのカテゴリの事後確率の対数 log(P(cat|doc)) を求める"""
      total = sum(self.catcount.values())  # 総文書数
      score = math.log(float(self.catcount[cat]) / total)  # log P(cat)
      for wc in doc:
         word, count = wc.split(":")
         count = int(count)
         # logをとるとかけ算は足し算になる
         for i in range(count):
            score += math.log(self.wordProb(word, cat))  # log P(word|cat)
      return score

   def __str__(self):
      total = sum(self.catcount.values())  # 総文書数
      return "documents: %d, vocabularies: %d, categories: %d" % (total, len(self.vocabularies), len(self.categories))


# eval.py
# ナイーブベイズの性能評価

def evaluate(trainfile, testfile):
   # 訓練データをロード
   trainData = []
   fp = codecs.open(trainfile, "r", "utf-8")
   for line in fp:
      line = line.rstrip()
      temp = line.split()
      trainData.append(temp)
   fp.close()

   # ナイーブベイズを訓練
   nb = NaiveBayes()
   nb.train(trainData)
   print(nb)
                                                              
   # テストデータを評価
   hit = 0
   numTest = 0
   fp = codecs.open(testfile, "r", "utf-8")
   for line in fp:
      line = line.rstrip()
      temp = line.split()
      correct = temp[0]    # 正解カテゴリ
      words = temp[1:]     # 文書：単語の集合
      predict = nb.classify(words)  # ナイーブベイズでカテゴリを予測
      if correct == predict:
         hit += 1  # 予測と正解が一致したらヒット！
      numTest += 1
   print("accuracy:", float(hit) / float(numTest))
   fp.close()

if __name__ == "__main__":
   evaluate("news20_noun", "news20_t_noun")
