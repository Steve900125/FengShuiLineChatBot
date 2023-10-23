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

from linebot import LineBotApi, WebhookHandler
# LineBotApi : 是用於建立和管理 Line 機器人的主要介面
# WebhookHandler : 用於處理 Line 機器人的 Webhook 請求
# 當有新的事件（例如用戶發送消息）發生時，Line 伺服器向你的應用程式發送的 HTTP POST 請求。
from linebot.exceptions import InvalidSignatureError
# InvalidSignatureError : 用於處理 Line Webhook 的簽名驗證錯誤
from linebot.models import MessageEvent, TextMessage, TextSendMessage
# MessageEvent : 表示 Line 機器人接收到的訊息事件
# TextMessage :  Line Bot 於表示文字訊息，使用這個類別來處理和回覆文字訊息
# TextSendMessage : 建立要發送的文字訊，將這個訊息傳送回 Line 伺服器，以回應用戶的請求

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

line_bot_api = LineBotApi(line_api)
handler = WebhookHandler(secrect_api)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)

# App route
#============================================================================#

# 當接收到一個 POST 請求時，它將從請求中獲取特定的標頭和數據，然後嘗試處理這些數據。
# 如果在處理過程中遇到任何問題，它將返回一個 400 Bad Request 的 HTTP 狀態碼。如果一切正常，它將返回 'OK' 字符串。
app.route("/callback" , methods = ["POST"])
def callbake():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 當使用者傳送訊息給Line Bot時，會觸發MessageEvent事件，這裡僅處理收到的文字訊息
@handler.add(MessageEvent , message = TextMessage)
def handle_message(event):
    line_bot_api.replay_message(event.reply_token,
        TextMessage(text = event.message.text))

@app.route("/hi")
def hi():
    return 'hi'

@app.route("/")
def home():
    return 'You are in home'

@app.route("/apikey")
def apikey_check():
    return 'line :' + line_api + '\n secrect_api:' + secrect_api


