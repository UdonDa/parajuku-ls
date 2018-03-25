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

#if __name__ == '__main__':
    #nakahiko = Nakahiko()
    #location = str(u"渋谷")
    #pripara_shops = nakahiko.get_pripara_shops(location)
    #print(pripara_shops['response'])

    #print(pripara_shops[0])
    #result = ''
    #for doc in pripara_shops:
    #    doc['hasGacha'] = "ある" if doc['hasGacha'] == "True" else "ない"
    #    result += "\n名前:{}\n住所:{}\nガチャは{}ぷり\n".format(doc['name'], doc['address'], doc['hasGacha'])

    #print(result)