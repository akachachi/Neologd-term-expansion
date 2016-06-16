from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

def hitcount(query):

    driver = webdriver.PhantomJS('phantomjs')

    sleep(1)
    driver.get("http://www.bing.com/")
    driver.find_element_by_name('q').send_keys(query)
    sleep(1)
    driver.find_element_by_name('q').send_keys("\n")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    #フレーズ検索のヒット件数が0で，キーワード検索に変換された時の対処
    hit_counts_string = ""
    if soup.find_all('span',class_="sb_count"):
        hit_counts_string = soup.find_all("span", class_='sb_count')[0].string
    else:
        hit_counts_string = "0" #class = bo

    driver.quit()

    #取得したヒット件数を整形(6,240,000 件の検索結果 のようになっている)
    temp = ""
    for num in hit_counts_string.split(','):
        if "件" in num:
            temp += num.split(" ")[0]
        else:
            temp += num

    hit_count = int(temp)
    return hit_count
