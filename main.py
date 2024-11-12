# Flask import
#============================================================================#
from flask import Flask
from flask import request,abort

app = Flask(__name__)


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
    ImageMessage,
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
from agent_main import run_line_agent

import fengshui.assessment as fs
import aws_boto3.aws as aws
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

        agent_ans = run_line_agent(
            user_id=event.source.user_id,
            question=event.message.text,
            timestamp=event.timestamp
        )

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
        # delet user data
        if images_path.exists():
            shutil.rmtree(images_path)
            print(f"{images_path} has been deleted.")
            os.makedirs(images_path) 
        else:
            os.makedirs(images_path) 
        
        try :          
            line_bot_blob_api = MessagingApiBlob(api_client)
            message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
            save_dir = images_path / f"{event.message.id}.jpg"

            with open(save_dir, "wb") as img_file:
                img_file.write(message_content)
            
            fs_image_results = fs.run()

            response_prompt_fs = ""

            # 檢查對門煞與入口相沖廚房的問題
            door_num = len(fs_image_results['door_to_door'])
            ent_num = len(fs_image_results['entrance_to_kitchen'])

            # 檢查是否有對門煞的情況
            if door_num > 0:
                response_prompt_fs += "發現平面圖中出現對門煞，發現 {} 個類似情況，以下是原因與建議。".format(str(door_num))

            # 檢查是否有入口相沖廚房的情況
            if ent_num > 0:
                response_prompt_fs += "發現平面圖中出現大門相沖廚房，發現 {} 個類似情況，以下是原因與建議。".format(str(ent_num))

            messages = []

            # 如果有問題描述，將其加入 messages
            if response_prompt_fs:
                messages.append(TextMessage(text=response_prompt_fs))
                response_prompt_fs += '請幫我查詢風水問題的相關建議'
            else:
                response_prompt_fs = "目前一切正常沒有檢測到風水問題僅需回復沒有發現相關問題"

            # 總結問題提示並傳給 Agent_Run 取得回覆
            agent_ans = run_line_agent(
                user_id=event.source.user_id,
                question=response_prompt_fs,
                timestamp=event.timestamp
            )

            # 將 Agent 的回覆加入 messages
            messages.append(TextMessage(text=agent_ans))
   
            if door_num > 0:
                for image_path in fs_image_results['door_to_door']:
                    url = aws.upload_to_aws(local_file= str(image_path), 
                                            bucket_name= 'fschatbot', 
                                            s3_file=image_path.name)
                    
                    mes = ImageMessage(original_content_url= url , preview_image_url= url )
                    messages.append(mes)

            if ent_num > 0:
                for image_path in fs_image_results['entrance_to_kitchen']:
                    url = aws.upload_to_aws(local_file= str(image_path), 
                                            bucket_name= 'fschatbot', 
                                            s3_file=image_path.name)  
                    mes = ImageMessage(original_content_url= url , preview_image_url= url )
                    messages.append(mes)

            # 發送訊息
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages  # 傳遞所有組合的訊息，包括文字與圖片
                )
            )
        
            
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
