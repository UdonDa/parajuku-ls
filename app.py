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
        location = event.message.text
        nakahiko = Nakahiko()
        reply_text = nakahiko.get_shops_info(location)
    except:
        reply_text = "えらーぷり。\n" + traceback.format_exc()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    import traceback
    
    reply_text = "わー！まだ東京しかたいおうしてないぷり！ごめんぷり！"
    try:
        tokyo_place = re.search(r".+都(.+?)[市|区]", event.message.address)
        if tokyo_place:
            reply_text = tokyo_place.group(1) + "ぷり。"
    except:
        reply_text = "えらーぷり。\n" + traceback.format_exc()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))


if __name__ == "__main__":
    app.run()
