import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

env_path = '../.env'
load_dotenv(dotenv_path = env_path)
SQL_URL = os.getenv("SQL_URL")

# user :
# user_id
# user_message
# timestamp

# agent :
# agent_id
# agent_message
# timestamp

def save_data(user : dict ,  agent : dict):
    user_insert_sql = '''
            INSERT INTO usermessage(user_id,user_message,timestamp)
            VALUES ( %s , %s , %s )
            RETURNING *;
    '''
    agent_insert_sql = '''
            INSERT INTO agentmessage(user_id,agent_message,timestamp)
            VALUES ( %s , %s , %s )
            RETURNING *;
    '''
    
    try:
        # connect to database
        conn = psycopg2.connect(SQL_URL)
        cursor = conn.cursor()
        
        # Formate
        timestamp_dt = datetime.fromtimestamp(user['timestamp'] / 1000.0) 

        user_save_data = (user['user_id'],user['user_message'],timestamp_dt,)
        agent_save_data = (user['user_id'],agent['agent_message'],timestamp_dt,)

        cursor.execute(user_insert_sql , user_save_data)
        print('#user: '+ cursor.fetchall())
        cursor.execute(agent_insert_sql , agent_save_data)
        print("#agent: "+ cursor.fetchall())
        conn.commit()

        cursor.close()
        conn.close()
        print(f"PostgreSQL Inserting Success")
        
    except (Exception, psycopg2.Error) as error:
        print(f"Error PostgreSQL Inserting Fail: {error}")




