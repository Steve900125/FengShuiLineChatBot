# Flask import
#============================================================================#
from flask import Flask
app = Flask(__name__)
from flask import request,abort
# reques : 處理 HTTP 請求
# abort : 處理錯誤情況 ex: 404 not found

import json
# 載入 json 標準函式庫，處理回傳的資料格式

# Line bot SDK import
#============================================================================#

from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

# Api key setting
#============================================================================#

from dotenv import load_dotenv
# load_dotenv : 將敏感的帳密、主機位址或連線金鑰集中放在 .env 檔案隱藏資料 
import os 
# os : 提供了許多與作業系統交互的功能，包括讀取、寫入檔案，創建目錄，執行系統命令等

load_dotenv()
# 載入 .env 檔
LINE_BOT_API_KEY = os.environ.get("LINE_BOT_API_KEY")
CHANNEL_SECRECT_KEY = os.environ.get("SLINE_BOT_API_KEY")

line_api = os.getenv("LINE_BOT_API_KEY" , LINE_BOT_API_KEY)
secrect_api = os.getenv("CHANNEL_SECRECT_KEY" , CHANNEL_SECRECT_KEY)
# 取得 api key

configuration = Configuration(access_token=line_api)
# 'MY_CHANNEL_ACCESS_TOKEN'
handler = WebhookHandler(secrect_api)
# 'MY_CHANNEL_SECRET'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)

# App route
#============================================================================#

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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token = event.reply_token,
                messages=[TextMessage(text = event.message.text)]
            )
        )
        return "TextMessage(text = event.message.text) : " + TextMessage(text = event.message.text) + 'event.message.text'

@app.route("/hi")
def hi():
    return 'hi'

@app.route("/")
def home():
    return 'You are in home'

@app.route("/apikey")
def apikey_check():
    return 'line :' + line_api + '\n secrect_api:' + secrect_api

@app.route("/test")
def test():
    result = ''
    # First SQL


