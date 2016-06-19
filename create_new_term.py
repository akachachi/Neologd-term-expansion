# coding: utf-8

import requests
import MeCab
from bs4 import BeautifulSoup
import csv

from bing_api import Bing
from ngram import text2words, wordNgram
from normalize_neologd import normalize_neologd



def main():
    
    """
    単語取得の出発点となるクエリを取得
    以下のURLは若者が使う新語・流行語一覧を記載している
    """
    query = []
    r = requests.get('http://bosesound.blog133.fc2.com/blog-entry-155.html')
    soup = BeautifulSoup(r.text, "html.parser")
    for li in soup.find_all('li'):
        query.append(li.string)


    """
    各クエリでの検索結果300件のタイトルとスニペットを取得
    """
    bing = Bing('enter Bing Search API Key here') #必須：api keyを入力
    text_set = []
    for q in query:
        search_results = bing.web_search(q, 300, ["Title", "Description"])
        for doc in search_results:
            #正規化をして追加する
            text_set.append(normalize_neologd(doc["Title"]))
            text_set.append(normalize_neologd(doc["Description"]))



    """
    text_setを用いて登録単語候補を作成する
    単語候補のパターンは分割された単語を2つつなげたもの
    """
    registration_word_candidate_by_bigram = []
    for text in text_set:
        words = text2words(text)
        ngram = wordNgram(words, 2)
        registration_word_candidate_by_bigram.extend(ngram)



    """
    候補を評価　そのフレーズに名詞と形容詞が計２つ存在するなら登録
    """
    registration_word = []
    for candidate in registration_word_candidate_by_bigram:
        mt = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
        node = mt.parseToNode(candidate)

        #名詞形容詞の数を数える
        num_of_meanigful = 0
        while node:
            feature = node.feature.split(',')
            if feature[0] == "名詞" or feature[0] == "形容詞":
                num_of_meanigful += 1
            node = node.next

        if num_of_meanigful == 2:
            registration_word.append(candidate)

    #重複を削除
    registration_word = list(set(registration_word))



    """
    辞書に追加する単語の読みを作成する
    """
    data = []
    for word in registration_word:
        mt = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
        node = mt.parseToNode(word)    
        kana = ""
        while node:
            feature = node.feature.split(',')
            #読みがないものは採録しないので＊で判別する
            if len(feature) >= 8:
                kana += feature[7]
            else:
                kana += "*"

            node = node.next
    
        #最初と最後のBOS/EOSに関するものを削除
        kana = kana[1:-1]

        if "*" not in kana:
            data.append([word, kana])


    """
    データ書込
    """
    with open('new_words.txt', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)

    return





if __name__ == '__main__':

    main()


