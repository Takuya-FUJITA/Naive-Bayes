import MeCab

text = 'メロンパン'
m = MeCab.Tagger('-d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd')
m_text = m.parse(text)

# マッピングの処理
text_dict = {}
for row in m_text.split('\n'):
   if row == 'EOS':
      break
   word = row.split('\t')[0]
   hinsi = row.split('\t')[1].split(',')[0]
   text_dict[word] = hinsi

# 出力
for w in text_dict.keys():
   print('「{}」の品詞は{}です。' .format(w, text_dict[w]))
