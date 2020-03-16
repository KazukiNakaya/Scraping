#!/usr/bin/env python3

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import os

class Ramen_db:

    def __init__(self, base_url, begin_page=1, prefecture = None, tag = 3): #tag 2:家系 ,3:二郎系
        
        # 変数宣言
        self.columns = ['name', 'url', 'ratingValue', 'latitude', 'longitude', 'addres']
        self.df = pd.DataFrame(columns=self.columns)

        page = begin_page
        list_url = []

        t1 = time.time()

        while True:
        #while page != 3:
            
            print(f"{page}ページ目の情報を取得中")

            #店舗一覧ページ(list_page)のURLを取得
            list_url = self.get_list_url(base_url, page, prefecture, tag)

            #店舗一覧ページをスクレイピング
            shop_url_list = self.scrape_list(base_url, list_url)

            #店舗URLが見つからない場合
            if shop_url_list == 0:
                break
            page+=1

        t2 = time.time()

        scraping_time = t2 - t1
        print("データフレーム作成")
        print(f'経過時間：{scraping_time}s')


        #csvファイルに出力
        print("csvファイル出力中")

        try:
            os.makedirs("./output")
        except FileExistsError:
            pass

        now = datetime.datetime.now()
        filename = './output/ramen_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'
        self.df.to_csv(filename, encoding='utf_8_sig')

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
            for shop_url in shop_url_list:
                self.scrape_shop(shop_url)

    def scrape_shop(self, shop_url):

        #取得したい情報 店舗名 位置情報（緯度、経度） 店舗URL ポイント 住所

        #HTMLパーサーを構成
        res = urlopen(shop_url)
        soup = BeautifulSoup(res, "html.parser")

        #schema.orgの情報タグを取得
        contents_basic = soup.find(id = "contents-basic")
        schema_tag = contents_basic.find('script')
        schema = schema_tag.getText()

        #情報を取得
        contents = schema.split(",") #カンマで区切ってリスト化
        #print(contents)

        try:
            name = [s for s in contents if '"name"' in s][0][8:-1] #店舗名
            url = [s for s in contents if '"url"' in s][0][7:-1] #URL
            ratingValue = [s for s in contents if '"ratingValue"' in s][0][15:-1] #ポイント
            latitude = [s for s in contents if '"latitude"' in s][0][12:-1] #緯度
            longitude = [s for s in contents if '"longitude"' in s][0][13:-2] #経度
            addressRegion = [s for s in contents if '"addressRegion"' in s][0][17:-1] #都道府県
            addressLocality = [s for s in contents if '"addressLocality"' in s][0][19:-1] #市町村
            streetAddress = [s for s in contents if '"streetAddress"' in s][0][17:-1] #番地
            address = addressRegion + addressLocality + streetAddress #住所

            #name = contents[2][8:-1] #店舗名
            #url = contents[19][7:-1] #URL
            #ratingValue = contents[14][15:-1] #ポイント
            #latitude = contents[21][12:-1] #緯度
            #longitude = contents[22][13:-2] #経度
            #addressRegion = contents[6][17:-1] #都道府県
            #addressLocality = contents[7][19:-1] #市町村
            #streetAddress = contents[8][17:-1] #番地
            #address = addressRegion + addressLocality + streetAddress #住所

            #DataFrameにデータを追加
            add_list = [name, url, ratingValue, latitude, longitude, address]
            add_data = pd.DataFrame(add_list, index = self.df.columns).T
            self.df = self.df.append(add_data)
        except:
            pass

#インスタンスを作成
base_url = "https://ramendb.supleks.jp"
ramen_db = Ramen_db(base_url, begin_page=1, prefecture = None, tag = 3)