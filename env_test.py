from dotenv import load_dotenv
import os 

load_dotenv()


line_api_value = os.getenv("LINE_BOT_API_KEY")
secrect_api = os.getenv("CHANNEL_SECRECT_KEY")
host = os.getenv("SQL_HOST")
port = os.getenv('SQL_PORT')
user = os.getenv("SQL_USER")
password = os.getenv("SQL_PASSWORD")

if line_api_value != None:
    print('line api .env : pass')
else :
    print('line api .env : fail')

if secrect_api  != None:
    print('secrect_api  .env : pass')
else :
    print('secrect_api  .env : fail')
    
if host != None and port != None and user != None and password != None:
    print('SQL data .env : pass')
else :
    print('SQL data .env : fail')





