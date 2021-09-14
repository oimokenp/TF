# coding=utf-8

import csv
import MeCab

ignores = []
ignores_words_files = 'stop_word.txt'
with open(ignores_words_files, 'r') as f:
    ignores = [line.strip() for line in f]

#mecabインスタンス作成
me = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

count_noun = dict()#名詞
count_adjective = dict()#形容詞
count_verb = dict()#動詞
num = 1

with open('test.txt', 'r', encoding = 'utf-8') as f:
    for lines in f:
        lines = lines.strip('\n')
        text = []
        result = me.parse(lines)
        result = result.strip()
        result = result.replace('\t',',')
        result = result.split('\n')
        for word in result:
            word = word.split(',',11)
            if word[0] == 'EOS':
                break
            elif word[1] == '名詞':
                if word[2] == '数':
                    pass
                else:
                    i = word[7]
                    if i in count_noun:
                        count_noun[i] += 1
                    else:
                        count_noun[i] = 1
            elif word[1] == '形容詞':
                i = word[7]
                if i in count_adjective:
                    count_adjective[i] += 1
                else:
                    count_adjective[i] = 1
            elif word[1] == '動詞':
                i = word[7]
                if i in count_verb:
                    count_verb[i] += 1
                else:
                    count_verb[i] = 1
        print(num)
        num+=1

for i in ignores:
    try:
        del count_noun[i]
        del count_adjective[i]
        del count_verb[i]
    except Exception as e:
        print(e)
        pass

sum_noun = sum(count_noun.values())
sum_adjective = sum(count_adjective.values())
sum_verb = sum(count_verb.values())

#CSVファイルに記入
with open('tf_noun_me.csv', 'w',encoding='sjis') as f:
    writer = csv.DictWriter(f, fieldnames = ['hinsi', 'count'])
    for key, value in sorted(count_noun.items(), key = lambda x:-x[1]):
        writer.writerow({'hinsi':key, 'count':value/sum_noun})

with open('tf_adjective_me.csv', 'w',encoding='sjis') as f:
    writer = csv.DictWriter(f, fieldnames = ['hinsi', 'count'])
    for key, value in sorted(count_adjective.items(), key = lambda x:-x[1]):
        writer.writerow({'hinsi':key, 'count':value/sum_adjective})

with open('tf_verb_me.csv', 'w',encoding='sjis') as f:
    writer = csv.DictWriter(f, fieldnames = ['hinsi', 'count'])
    for key, value in sorted(count_verb.items(), key = lambda x:-x[1]):
        writer.writerow({'hinsi':key, 'count':value/sum_verb})