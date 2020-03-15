#!/usr/bin/env python3

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

class Ramen_db:

    def __init__(self, base_url, begin_page=1, prefecture = None, tag = 3): #tag 2:家系 ,3:二郎系
        
        # 変数宣言
        self.columns = ['store_id', 'store_name', 'score', 'ward', 'review_cnt', 'review']
        self.df = pd.DataFrame(columns=self.columns)

        page = begin_page
        list_url = []

        while True:
        
            #店舗一覧ページ(list_page)のURLを取得
            list_url = self.get_list_url(base_url, page, prefecture, tag)

            #店舗一覧ページをスクレイピング
            shop_url_list = self.scrape_list(base_url, list_url)

            #店舗URLが見つからない場合
            if shop_url_list == 0:
                break



            page+=1




            #res = requests.get(url)

            #ページが存在しなくなったらクローリング終了
            #if res.status_code != requests.codes.ok:
            #    break
            #else:
            #    list_url.append(url)
            #
            #page+=1

        print("url一覧取得完了")

    def get_list_url(self, base_url, page, prefecture = None, tag=3): 

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
        list_url = base_url + page_text + state + tag_text

        return list_url

    def scrape_list(self, base_url, list_url):

        #HTMLパーサーを構成
        res = urlopen(list_url)
        soup = BeautifulSoup(res, "html.parser")
        #print(soup.prettify()) #htmlを整形して表示

		#テーブルヘッダ"<div class="area">"を起点に店舗URLリストを取得する
        shop_url_list = []
        for th in  soup.find_all(class_="photo"):
            tag = th.find('a')
            url = base_url + tag.get("href")
            shop_url_list.append(url)

        if len(shop_url_list) == 0: #店舗URLが見つからない場合
            return 0
        else:
            self.scrape_shop(base_url, shop_url_list)

    def scrape_shop(self, shop_url_list):
        pass



#インスタンスを作成
base_url = "https://ramendb.supleks.jp"
ramen_db = Ramen_db(base_url, begin_page=1, prefecture = None, tag = 3)