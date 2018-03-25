#!/usr/bin/env python
# coding: utf-8
try:
    from urllib.request import *
    from urllib.parse import *
    import json
    import argparse
    import requests
except Exception:
    print("うわー")
    exit()

class Nakahiko():
    def __init__(self):
        self.base_url = "https://script.google.com/macros/s/AKfycbwoTfLoZJEktYH_RQq0BNStXFHCKhRi9rC1Sb16xsc2LGbepTU/exec?callback=receiveJson&keyword="

    def send_request(self, url):
        try:
            response = requests.get(url)
            doc = response.text
            return doc
        except HTTPErrorProcessor:
            print("404")
            return None

    def make_request_url(self, location):
        url = "{}".format(self.base_url)
        url += "{}".format(location)

        return url

    def convert_to_json(self, result):
        # 最初の方に無駄な文字列が入っており, それを取り除いて, jsonに型を変える
        return json.loads(result[12:-1])

    def get_pripara_shops(self, location):
        """
        :param location (ex)渋谷:
        :return: json
        """
        url = self.make_request_url(location)
        result = self.send_request(url)
        result = self.convert_to_json(result)
        return result['response']

    def get_shops_info(self, location):
        """
        :param location: str
        :return: str
        """
        pripara_shops = self.get_pripara_shops(location)
        reply_text = "わー！"
        if pripara_shops:
            reply_text = ""
            address_base = 'http://maps.google.co.jp/maps?q='
            i = 0
            for shop in pripara_shops:
                if i < 6:
                    shop['hasGacha'] = "ある" if shop['hasGacha'] == "True" else "ない"
                    shop['address'] = shop['address'].replace('　', ',')
                    reply_text += "\n名前 : {}\n住所 : {}\nガチャは{}ぷり\n{}{}\n".format(shop['name'], shop['address'],
                                                                                shop['hasGacha'], address_base,
                                                                                shop['address'])
                i += 1
        return reply_text

#if __name__ == '__main__':
    #nakahiko = Nakahiko()
    #location = str("未来")
    #pripara_shops = nakahiko.get_pripara_shops(location)
    #result = ''
    #for doc in pripara_shops:
    #    doc['hasGacha'] = "ある" if doc['hasGacha'] == "True" else "ない"
    #    result += "\n名前:{}\n住所:{}\nガチャは{}ぷり\n".format(doc['name'], doc['address'], doc['hasGacha'])
    #print(pripara_shops)
    #if pripara_shops:
    #    print("True")
    #elif not pripara_shops:
    #    print("False")