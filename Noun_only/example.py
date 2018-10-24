import treetaggerwrapper
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='/usr/local/src/tree-tagger')
tags = tagger.TagText("He is trying to find some graphics software on PC. Any suggestion on which software to buy,where to buy and how much it costs ?")
d = ["NN","NNS","NP","NPS"]
for tag in tags:
   a,b,c = tag.split('\t')
   """
   print(a,end=" ")
   print(b,end=" ")
   print(c)
   """
   if b in d:  #$B<B:]$K<B83$GMQ$$$?7A(B
      print(a)
