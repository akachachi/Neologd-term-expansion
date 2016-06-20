NEologd-term-expansion
====

## Description
`NEologd-term-expansion` is CLI tool that automatically extracts words which are not accepted in NEologd from Web pages. This outputs words in *new_words.txt*.

## Requirement
- Python 3.5.1

## Usage

### Step.1
Install ***mecab-ipadic-NEologd*** in reference to the URL,`https://github.com/neologd/mecab-ipadic-neologd`.

### Step.2

```
$ git clone https://github.com/akachachi/Neologd-term-expansion.git
$ cd NEologd-term-expansion
$ python3 create_new_term.py "BingSearchAPIKey"
```
- It takes about an hour to create terms.
- In order to run this program, you need to get API key for Bing Search API.

