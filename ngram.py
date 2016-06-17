import MeCab

def text2words(text):
    mt = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
    mt.parse('')
    node = mt.parseToNode(text)

    words = []
    while node:
        words.append(node.surface)
        node = node.next

    return words


#単語の配列に対してNgramを作成する
def wordNgram(words, N):
    
    ngram = []

    for i in range(len(words)-N+1):
        phrase = ''
        for j in range(N):
            phrase += words[i+j]

        ngram.append(phrase)

    return ngram


