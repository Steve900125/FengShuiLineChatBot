import langchain
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()
# 載入 .env 文件
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# 取得 .env 內 API_KEY
openai.api_key = os.getenv('OPENAI_API_KEY', OPENAI_API_KEY)


# user_data 聊天記錄
# user_question 使用者從 line 傳出的文字 text string
def call_chatgpt( user_data : list , user_question : str , user_id : str):
    response_text = ''
    messages = []
    functions = []


# Load user_data and user_question
#============================================================================#
    question = { "role": "user", "content": user_question }
    messages.append(question)

# Use openai to get response from gpt
#============================================================================#
    try:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            # This is the chat message from the user
            messages = messages  
            #functions = functions,
            #function_call = "auto",
        )
        response_text = response['choices'][0]['message']['content']
    except Exception as e:
        print(e)
        response_text = 'call faile'


    
    return response_text