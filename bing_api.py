# -*- coding: utf-8 -*-
import urllib
import requests
import json


class Bing(object):
    # コンストラクタ（初期化）
    def __init__(self, key):
        self.api_key = key

    # web検索
    def web_search(self, query, k, keys=["Url"], skip=0):
        """
            keysには'ID','Title','Description','DisplayUrl','Url'が入りうる
        """
        # 基本になるURL
        url = 'https://api.datamarket.azure.com/Bing/Search/v1/Composite?Sources=%27Web%27&'
        # 一回で返ってくる最大数
        max_num = 50
        # 各種パラメータ
        params = {
            "Query": "'{0}'".format(query),
            "Market": "'ja-JP'"
        }
        # フォーマットはjsonで受け取る
        request_url = url + urllib.parse.urlencode(params) + "&$format=json"
        results = []

        # 最大数でAPIを叩く繰り返す回数
        repeat = int((k - skip) / max_num)
        remainder = (k - skip) % max_num

        # 最大数でAPIを叩くのを繰り返す    
        for i in range(repeat):
            result = self._search(request_url, max_num, max_num * i, keys)
            results.extend(result)
        # 残り
        if remainder:
            result = self._search(request_url, remainder, max_num * repeat, keys)
            results.extend(result)

        return results

    # 関連クエリ
    def related_search(self, query, keys=["Title"]):
        """
            keysには'ID','Title','BaseUrl'が入りうる
        """
        # 基本になるURL
        url = 'https://api.datamarket.azure.com/Bing/Search/RelatedSearch?'
        # 各種パラメータ
        params = {
            "Query": "'{0}'".format(query),
            "Market": "'ja-JP'"
        }
        # フォーマットはjsonで受け取る
        request_url = url + urllib.parse.urlencode(params) + "&$format=json"
        results = self._search(request_url, 50, 0, keys)
        return results

    # APIを叩く
    def _search(self, request_url, top, skip, keys):
        # APIを叩くための最終的なURL
        final_url = "{0}&$top={1}&$skip={2}".format(request_url, top, skip)
        response = requests.get(final_url, 
                                auth=(self.api_key, self.api_key), 
                                headers={'User-Agent': 'My API Robot'}).json()
        results = []
        # 返ってきたもののうち指定された情報を取得する
        for item in response["d"]["results"][0]["Web"]:
            result = {}
            for key in keys:
                result[key] = item[key]
            results.append(result)
        return results


if __name__ == '__main__':
    key = '<キー>'
    q = "京都"
    bing = Bing(key)
    results = bing.web_search(q, 100, ["Title", "Url"])
    print(json.dumps(results, indent=2))
    results = bing.related_search(q)
    print(json.dumps(results, indent=2))
