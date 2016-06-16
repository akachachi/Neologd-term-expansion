# coding: utf-8


import requests
import MeCab
from bs4 import BeautifulSoup
from selenium import webdriver

from bing_api import Bing
from ngram import text2words, wordNgram


if __name__ == '__main__':
    
    #単語取得の出発点となるクエリを取得
    query = []
    r = requests.get('http://bosesound.blog133.fc2.com/blog-entry-155.html')
    soup = BeautifulSoup(r.text, "html.parser")
    for li in soup.find_all('li'):
        query.append(li.string)


    #，や（）で句切られているものがあるので，出発点のクエリを整形

    query = ['あなる']
    #各クエリで検索結果のタイトルとスニペットを取得
    bing = Bing('oRqVUnUoJuoHsbY/fnRxFLqEHjdDYeBz66ksaNtBwh4')
    text_set = []
    for q in query:
        search_results = bing.web_search(q, 10, ["Title", "Description"])
        for doc in search_results:
            #正規化必要
            text_set.append(doc["Title"])
            text_set.append(doc["Description"])


    #text_setを用いて登録単語候補を作成する
    registration_word_candidate = []
    for gram in range(1,11):
        for text in text_set:
            words = text2words(text)
            ngram = wordNgram(words, gram)
            registration_word_candidate.extend(ngram)

    print(registration_word_candidate)
    #作成した候補を評価する


    #辞書に追加することが決まった単語の読みを作成する


    #csvデータに書き込む



    
