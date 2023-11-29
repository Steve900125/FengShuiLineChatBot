# Flask import
#============================================================================#
from flask import Flask
from flask import request,abort

app = Flask(__name__)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)


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
    
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
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


# ChatGPT call import
#============================================================================#
# from functions.chatgpt_response import call_chatgpt

# postgresql call import
#============================================================================#
from functions.postgresql_function import save_data , get_user_messages

# LangChain function call 
#============================================================================#
# Import things that are needed generically
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from functions.RealEstate_Recommendation import RealEstateRecommendationTool
# gpt-3.5-turbo-0613
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder



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
# Keyword : Get user name / User Name / User ID 
#============================================================================#
        try :
            url = 'https://api.line.me/v2/bot/profile/' + event.source.user_id
            # 把傳入的使用者 id 當作參數用 api 去取得用戶資料名稱
            headers = {
                'Authorization': 'Bearer ' + line_api_value 
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
# keyword : Chat history / User Messages / Agent Messages / Database  / Postgresql
#============================================================================#
        try:
            agent_kwargs = {
                "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
            }
            memory = ConversationBufferMemory(memory_key="memory", return_messages=True)


            chat_history = get_user_messages(event.source.user_id)
            # User message : row_data[0]
            # Agent message : row_data[1]
            for row_data in chat_history :
                memory.save_context({"input": row_data[0]}, {"output": row_data[1]})
        except Exception as e:
            print('Database load data fail 取得使用者紀錄失敗')
            print(e)
     

# Call LangChain Agent (chatGPT) to answer the question 
# Maybe can select which models suit the question type
# keyword : Tools / Agent / LangChain / ChatGPT 
#============================================================================# 
        try :
            model = ChatOpenAI( 
                model="gpt-4-1106-preview" ,
                temperature= 0.9
            )
            tools = [RealEstateRecommendationTool()]
            agent = initialize_agent(tools, 
                            model, 
                            agent= AgentType.OPENAI_FUNCTIONS, 
                            verbose= False,
                            memory = memory,
                            agent_kwargs = agent_kwargs

            )
            agent_ans = agent.run(event.message.text)
        
        except Exception as e :
            print("Call LangChain Agent Fail")
            print(e)
            agent_ans = '伺服器維修中'
        

# Return response to user
# Keyword : Return / Response / Line Response / MessagingApi
#============================================================================#
        try :
            line_bot_api = MessagingApi(api_client)     
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token = event.reply_token,
                    messages=[TextMessage(text = user_name + agent_ans )]
                    # 回傳資料的地方
                )
            )            
        except Exception as e:
            print('Return response to user (TextMessageContent) Fail')
            print(e)

 # Save user and agent message
 # Keyword : Save Data / Save Chat History / Database / Postgresql
#============================================================================# 
        try:
            user = {
                "user_id" : event.source.user_id , 
                "user_message": event.message.text , 
                "timestamp" : event.timestamp
            }
            agent = {
                "agent_message" : agent_ans 
            }
            save_data(user = user , agent = agent)

        except Exception as e:
            print('Save user and agent message Fail')
            print(e)


    

