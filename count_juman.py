# coding=utf-8

import csv
import subprocess

def juman(Text):
    P = subprocess.Popen(["juman"], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    P.stdin.write(Text)
    P.stdin.close()
    Result = P.stdout.read()
    return Result.decode("sjis")

ignores = []
ignores_words_files = 'stop_word.txt'
with open(ignores_words_files, 'r') as f:
    ignores = [line.strip() for line in f]

Result = []

count_noun = dict()#名詞
count_adjective = dict()#形容詞

for num in range(0,101):
    for line in open("test.txt","rb"):
        r = juman(line)
        r = r.strip()
        r = r.split("\n")
        for word in r:
            word = word.split(None, 11)#空文字で文字列を区切る
            if word[0] == 'EOS':
                break
            elif word[3] == '名詞': #４番目に品詞が来るので
                i = word[0]
                if i in count_noun:
                    count_noun[i] += 1
                else:
                    count_noun[i] = 1
            elif word[3] == '形容詞':
                i = word[0]
                if i in count_adjective:
                    count_adjective[i] += 1
                else:
                    count_adjective[i] = 1

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