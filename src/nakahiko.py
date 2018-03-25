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
            #print("---------------{}---------------".format(urlopen(url)))

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

    def send_request_to_nakahiko(self, location):
        """
        :param location (ex)渋谷:
        :return: request
        """
        url = self.make_request_url(location)
        return self.send_request(url)

if __name__ == '__main__':
    nakahiko = Nakahiko()
    location = str(u"渋谷")
    result = nakahiko.send_request_to_nakahiko(location)
    #res_decoded = result.decode("utf-8")
    print(result)