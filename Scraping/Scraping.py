#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pandas as pd

class Ramen_db:

    def __init__(self, base_url, begin_page=1, prefecture = None, tag = 3): #tag 2:家系 ,3:二郎系
        
        # 変数宣言
        self.columns = ['store_id', 'store_name', 'score', 'ward', 'review_cnt', 'review']
        self.df = pd.DataFrame(columns=self.columns)

        page = begin_page

        while True:
        
            #店舗一覧ページのURLを取得
            list_url = self.get_url(base_url, page, prefecture, tag)
            res = requests.get(list_url)
            #ページが存在しなくなったらクローリング終了
            if r.status_code != requests.codes.ok:
                break
            page+=1

        print("url一覧取得完了")




    def get_url(self, base_url, page, prefecture = None, tag=3): 

        #開始ページ
        page_text = "/search?page=" + str(page)
        #都道府県
        if not prefecture == None:
            state = "&state=" + prefecture + "&city="
        else:
            state = ""
        #タグ
        if not tag == None:
            tag_text = "&order=point&station-id=0&tags=" + str(tag)
        else:
            tag_text = None     
        url = base_url + page_text + state + tag_text

        return url

    def scrape_list(self, list_url):

        #HTMLパーサーを構成
        res = req.urlopen(list_urll)
        soup = BeautifulSoup(res, "html.parser")

		#aaaaaを取得
        nameLevel = soup.find('div', id="name-level")
        userName = nameLevel.find('h2').string


#インスタンスを作成
base_url = "https://ramendb.supleks.jp"
ramen_db = Ramen_db(base_url, begin_page=1, prefecture = None, tag = 3)
#test 20200212