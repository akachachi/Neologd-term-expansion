import subprocess as sbp

def text2words(text):
    morp = sbp.getstatusoutput("echo " + text + " | mecab -Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")

    morps = morp[1].replace('\n', '')
    words = morps.split(' ')

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



if __name__ == '__main__':
    print(text2words("中居正広のタイトルから辛そうで辛くない少し辛いラー油"))
    print(wordNgram(text2words("中居正広のタイトルから辛そうで辛くない少し辛いラー油"), 2))
