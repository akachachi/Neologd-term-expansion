# coding: utf-8

import requests
import MeCab
from bs4 import BeautifulSoup
import csv

from bing_api import Bing
from ngram import text2words, wordNgram
from normalize_neologd import normalize_neologd


#mecabの辞書に登録されている単語は配列から除外する
def removeRegisterdWord(words):
    mt = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")

    word_for_del = []
    for word in words:
        node = mt.parseToNode(word)
        feature = node.next.feature.split(',')

        #読み仮名がある場合，辞書に登録されているので削除対象
        #記号，数もそれ単体では辞書に登録するほど意味が無いので削除対象
        if len(feature) >= 8 or feature[0] == "記号" or feature[1] == "数":
            word_for_del.append(word)

    #実際に単語を削除
    for word in word_for_del:
        words.remove(word)

    return words




def main():
    
    #単語取得の出発点となるクエリを取得
    query = []
    r = requests.get('http://bosesound.blog133.fc2.com/blog-entry-155.html')
    soup = BeautifulSoup(r.text, "html.parser")
    for li in soup.find_all('li'):
        query.append(li.string)


    #各クエリで検索結果のタイトルとスニペットを取得
    bing = Bing('oRqVUnUoJuoHsbY/fnRxFLqEHjdDYeBz66ksaNtBwh4')
    text_set = []
    for q in query:
        search_results = bing.web_search(q, 300, ["Title", "Description"])
        for doc in search_results:
            #正規化をして追加する
            text_set.append(normalize_neologd(doc["Title"]))
            text_set.append(normalize_neologd(doc["Description"]))

    #text_setを用いて登録単語候補を作成する
    registration_word_candidate_unigram =[]
    registration_word_candidate_Ngram = []
    for N in range(1,4):
        for text in text_set:
            words = text2words(text)
            ngram = wordNgram(words, N)

            #N=1のとき，mecabに分割はされるが読み仮名がついていないものは辞書に未登録
            #記号や数の場合も除外対象
            #読み仮名がすでに振られている単語は登録済みなので除外する
            if N == 1:
                registration_word_candidate_unigram.extend(removeRegisterdWord(ngram))
            else:
                registration_word_candidate_Ngram.extend(ngram)

    #候補を評価 フレーズ検索結果が1000件あれば追加単語とする
 #   registration_word = []
 #   for candidate in registration_word_candidate:
 #       phrase_query = "\"" + candidate + "\""
 #       hit_count = hitcount(phrase_query)
 #
 #       if hit_count >= 1000 :
 #           print(candidate)
 #           registration_word.append(candidate)



    mt = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
    #候補を評価　そのフレーズに名詞と形容詞が計２つ以上なら登録
    registration_word = []
    for candidate in registration_word_candidate_Ngram:
        node = mt.parseToNode(candidate)

        #名詞形容詞の数を数える
        num_of_meanigful = 0
        while node:
            feature = node.feature.split(',')
            if feature[0] == "名詞" or feature[0] == "形容詞":
                num_of_meanigful += 1
            node = node.next

        #数に応じて登録する単語を選択
        if num_of_meanigful >= 2:
            registration_word.append(candidate)

    #重複を削除
    registration_word = list(set(registration_word_candidate_unigram + registration_word))


    #辞書に追加する単語の読みを作成する
    registration_word_kana = []
    for word in registration_word:
        node = mt.parseToNode(word)    
        kana = ""
        while node:
            feature = node.feature.split(',')
            #読みがないものは * を代用
            if len(feature) >= 8:
                kana += feature[7]
            else:
                kana += "*"

            node = node.next
    
        #最初と最後のBOS/EOSに関するものを削除
        kana = kana[1:-1]
        registration_word_kana.append(kana)

    #書き込みやすいように整形
    data = []
    for i in range(len(registration_word)):
        data.append([registration_word[i], registration_word_kana[i]])

    #データ書込
    with open('new_words.txt', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)

    return





if __name__ == '__main__':

    main()


