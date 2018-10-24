#参考文献
#https://katsumin-prg.com/programming/mecab-tweet-count/

import MeCab
import re
import csv


# csvファイルを読み込む
# 戻り値は ツイートのデータのリスト
def file_open():
    file = open('./csv_data/9_15/2013_09_15.csv', encoding="utf-8") # csvファイルは文字化けするのでutf-8にエンコード
    #file = open('./csv_data/2013_07_23_other.csv', encoding="utf-8") # csvファイルは文字化けするのでutf-8にエンコード

    csv_reader = csv.reader(file)
    data = list(csv_reader)

    return data

# ツイートを分かち書きにしてリスト化する
def division(tweet):
    global word_list

    m = MeCab.Tagger('-d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd')
    s = m.parse(tweet)
    s = s.split('\n')

    # 省くもの t co ー http https
    # ↑は実際に実行してみて不要と感じた一般名詞であり、排除する

    for i in s:
        i = re.split('[\t,]', i)  # リストにするため空白と","で分割する。 'python　名詞, 一般, *, *, *, *, *' → ['python', '名詞', '一般', '*', '*', '*', '*', '*']
        if i[0] == 'EOS' or i[0] == '' or i[0] == 't' or i[0]=='co' or i[0] =='ー' or i[0] == 'http' or i[0] == 'https':
            pass
        elif i[1] == '名詞' and i[2] == '一般': # 一般名詞の単語をリストに追加する
        #elif i[1] == '名詞': # 一般名詞の単語をリストに追加する
            word_list.append(i)


# 単語の数をカウント
def word_count(tl):
    global dicts

    for i in tl:
        if i[0] not in dicts: # 辞書に入っていなければ値を1にする
            dicts.setdefault(i[0], 1)
        else: # 辞書に入っているならインクリメントする
            dicts[i[0]] += 1


if __name__ == '__main__':
    tweet_data = file_open() # ツイートデータを取得

    word_list = [] # 一般名詞を格納するリスト
    for i in tweet_data:
        division(i[1]) # division()関数にツイートを送り分割する i[5]にはtextが入っている

    dicts = {} # 単語をカウントする辞書
    word_count(word_list) # 単語をカウントする

    # 辞書を降順に出力
    j = 0
    with open('output.txt', mode='w') as f:
        for k, v in sorted(dicts.items(), key=lambda x: -x[1]):
            if j < 100:
                f.write(str(k) + '\n')
                #print(str(k) + ": " + str(v))
            j += 1
