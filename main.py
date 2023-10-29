# Flask import
#============================================================================#
from flask import Flask
app = Flask(__name__)
from flask import request,abort
# reques : 處理 HTTP 請求
# abort : 處理錯誤情況 ex: 404 not found

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)

import json
# 載入 json 標準函式庫，處理回傳的資料格式

import requests
# 用來取得外部連結 URL API 資料

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
    TextMessage,
    
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent
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

count = 0
# 測試數量限制 5 

# ChatGPT call import
#============================================================================#
from chatgpt_response import call_chatgpt




# callback : Hang on the web address on Line Webhook
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


# When the user sends the messages, this code will be activated.
#============================================================================#
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
# 取得使用者名稱
#============================================================================#
        try :
            url = 'https://api.line.me/v2/bot/profile/' + event.source.user_id
            # 把傳入的使用者 id 當作參數用 api 去取得用戶資料名稱
            headers = {
                'Authorization': 'Bearer ' + line_api
                }
            # channel access token 授權
            response = requests.get(url, headers = headers)

            user_name = 'Hello !'
            if response.status_code == 200:
                user_profile = response.json()
                user_name = user_name + user_profile['displayName'] + " 以下是您的訊息紀錄： "   
        except Exception as e:
            print('Get user name fail')
            print(e)

# Database load data
# Maybe lode user data by ID then check meassages
#============================================================================#
     

# Call chatGPT to answer the question
# Maybe can select which models suit the question type
#============================================================================#   
        try :
            global count
            if event.message.type == 'text' and count < 5:
                #ans = call_chatgpt(user_question = event.message.text , user_data = [] ,user_id = '')
                ans = 'chatGPT'
                count = count + 1
            else:
                ans = '今日使用上限已額滿' 
        except Exception as e:
            ans = ''
            print("Generate responses fail")
            print(e)
        
        print(ans)

# Return response to user
#============================================================================#
        try :
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token = event.reply_token,
                    messages=[TextMessage(text = user_name + ans + event.message.type)]
                    # 回傳資料的地方
                )
            )
        except Exception as e:
            print('LineBot return fail')
            print(e)
        
        print(type(event.message.text))
        print(event.message.text)
        print(type(event))
        print(f'Event: {event}')
        print(type(event.message))
        print(event.message)
        print('user id' + event.source.user_id)

@handler.add(MessageEvent, message= ImageMessageContent)
def handle_image_message(event):
    with ApiClient(configuration) as api_client:
        # 處理貼圖消息的代碼
        try :
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token = event.reply_token,
                        messages=[TextMessage(text = '你好棒 照片')]
                        # 回傳資料的地方
                    )
                )
        except Exception as e:
                print('LineBot return fail')
                print(e)
        
        print(type(event.message.text))
        print(event.message.text)
        print(type(event))
        print(f'Event: {event}')
        print(type(event.message))
        print(event.message)
        print('user id' + event.source.user_id)


@app.route("/testweb")
def testweb():
    gpt_ans = call_chatgpt(user_question = '請問狗狗跑多快？' , user_data = [] ,user_id = '')
    return gpt_ans


    

