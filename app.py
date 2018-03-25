import os
import sys
from flask import Flask, request, abort
import re
from urllib.request import *
from urllib.parse import *
import json
import argparse
import requests
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage

)
from src.nakahiko import Nakahiko

app = Flask(__name__)

# 環境変数からchannel_secret・channel_access_tokenを取得
channel_secret = os.environ['LINE_CHANNEL_SECRET']
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/")
def hello_world():
    return 'hello world'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    import traceback
    reply_text = "わー！まだ東京しかたいおうしてないぷり！ごめんぷり！"
    try:
        text = event.message.text
        nakahiko = Nakahiko()
        pripara_shops = nakahiko.get_pripara_shops(text)
        if pripara_shops:
            reply_text = ''
            for shop in pripara_shops:
                shop['hasGacha'] = "ある" if shop['hasGacha'] == "True" else "ない"
                reply_text += "\n名前 : {}\n住所 : {}\nガチャは{}ぷり\n".format(shop['name'], shop['address'], shop['hasGacha'])
    except:
        reply_text = "えらーぷり。\n" + traceback.format_exc()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()