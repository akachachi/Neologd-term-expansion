# coding: utf-8

import requests
import MeCab
from bs4 import BeautifulSoup

from bing_api import Bing
from ngram import text2words, wordNgram
from bing_hitcount import hitcount


#mecabの辞書に登録されている単語は配列から除外する
def removeRegisterdWord(words):
    mt = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")

    word_for_del = []
    for word in words:
        node = mt.parseToNode(word)
        feature = node.next.feature.split(',')
        if len(feature) >= 8:
            word_for_del.append(word)

    for word in word_for_del:
        words.remove(word)

    return words



if __name__ == '__main__':
    
    #単語取得の出発点となるクエリを取得
    query = []
    r = requests.get('http://bosesound.blog133.fc2.com/blog-entry-155.html')
    soup = BeautifulSoup(r.text, "html.parser")
    for li in soup.find_all('li'):
        query.append(li.string)


    #，や（）で句切られているものがあるので，出発点のクエリを整形，せんでええ！！

    query = ['中居正広']
    #各クエリで検索結果のタイトルとスニペットを取得
    bing = Bing('oRqVUnUoJuoHsbY/fnRxFLqEHjdDYeBz66ksaNtBwh4')
    text_set = []
    for q in query:
        search_results = bing.web_search(q, 10, ["Title", "Description"])
        for doc in search_results:
            #正規化必要
            text_set.append(doc["Title"])
            print(doc["Title"])
            text_set.append(doc["Description"])


    #text_setを用いて登録単語候補を作成する
    registration_word_candidate = []
    for N in range(1,6):
        for text in text_set:
            words = text2words(text)
            ngram = wordNgram(words, N)

            #N=1のとき，mecabに 分割はされるが読み仮名がついていないものは辞書に未登録
            #読み仮名がすでに振られている単語は登録済みなので除外する
            if N == 1:
                print(ngram)
                ngram = removeRegisterdWord(ngram)
                print(ngram)

            registration_word_candidate.extend(ngram)

    #print(registration_word_candidate)
    #作成した候補を評価する 1000件かなぁ
    for candidate in registration_word_candidate:

        phrase_query = "\"" + candidate + "\""
        hit_count = hitcount(phrase_query)
        print(hit_count, phrase_query)

    #辞書に追加することが決まった単語の読みを作成する


    #csvデータに書き込む



    
