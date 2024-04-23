# Flask import
#============================================================================#
from flask import Flask
from flask import request,abort

app = Flask(__name__)

import requests
# 用來取得外部連結 URL API 資料

# Line bot SDK import
#============================================================================#
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
    MessagingApiBlob
    
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent
    
)

# Api key setting
#============================================================================#
from dotenv import load_dotenv
import os 

load_dotenv()
line_api_value = os.getenv("LINE_BOT_API_KEY")
secrect_api = os.getenv("CHANNEL_SECRECT_KEY")


configuration = Configuration(access_token=line_api_value )
# 'MY_CHANNEL_ACCESS_TOKEN'
handler = WebhookHandler(secrect_api)
# 'MY_CHANNEL_SECRET'


# LangChain function call 
#============================================================================#
from langchain_agent import Agent_Run

import feng_shui as fs
import sys
import shutil
from pathlib import Path
import platform

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLO root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if platform.system() != 'Windows':
    ROOT = ROOT.relative_to(Path.cwd())


@app.route("/index")
def index():
    return "success !"


# callback : Hang on the web address on Line Webhook
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
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:

        agent_ans = Agent_Run(event.message.text , event.source.user_id , event.timestamp)

        # Return response to user
        # Keyword : Return / Response / Line Response / MessagingApi
        try :
            line_bot_api = MessagingApi(api_client)     
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token = event.reply_token,
                    messages=[TextMessage(text = agent_ans )]
                    # 回傳資料的地方
                )
            )            
        except Exception as e:
            print('Return response to user (TextMessageContent) Fail')
            print(e)




@handler.add(MessageEvent, message= ImageMessageContent)
def handle_image_message(event):
    with ApiClient(configuration) as api_client:
        
        images_path = ROOT / 'images'
        try :   
                
                line_bot_blob_api = MessagingApiBlob(api_client)
                message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)

                save_dir = images_path / f"{event.message.id}.jpg"
                with open(save_dir, "wb") as img_file:
                    img_file.write(message_content)
                
                fs_result = fs.run()

                door_problems = "對門煞 : 圖片發現 {0} 個類似情況，如果數值為零代表不存在或是圖片種類錯誤".format(str(fs_result['door'])) 
                door_advice = "發現平面圖中出現對門煞，發現 {0} 個類似情況，請給出原因合建議".format(str(fs_result['door']))
                
                agent_ans = Agent_Run( door_advice  , event.source.user_id , event.timestamp)

                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token = event.reply_token,
                        messages=[ TextMessage(text = door_problems) , TextMessage(text = agent_ans)]
                        # 回傳資料的地方
                    )
                )

                # delet user data
                if images_path.exists():
                    shutil.rmtree(images_path)
                    print(f"{images_path} has been deleted.")
                    os.makedirs(images_path)     
            
        except Exception as e:
                
                # delet user data
                if images_path.exists():
                    shutil.rmtree(images_path)
                    print(f"{images_path} has been deleted.")
                    os.makedirs(images_path) 

                print('LImageMessageContent Fail')
                print(e)

if __name__ == '__main__':
    app.run()
