import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

# 臭小子
if __name__ == '__main__':
    env_path = '../.env'
else :
    env_path = './.env'

load_dotenv(dotenv_path = env_path)
SQL_URL = os.getenv("SQL_URL")

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
        print('#user: '+ str(cursor.fetchall()))
        cursor.execute(agent_insert_sql , agent_save_data)
        print("#agent: "+ str(cursor.fetchall()))
        conn.commit()

        cursor.close()
        conn.close()
        print(f"PostgreSQL Inserting Success")
        
    except (Exception, psycopg2.Error) as error:
        print(f"Error PostgreSQL Inserting Fail: {error}")

def get_user_messages( user_id : str):
    user_target = (user_id,)
    # Use JOIN to get Messages by user_id
    # The value contain user and agent
    # Time can be the condition to descide which one needed to group togather . 
    sql_join = '''
        SELECT 
            usermessage.user_message,
            agentmessage.agent_message
        FROM 
            usermessage
        INNER JOIN 
            agentmessage ON usermessage.user_id = agentmessage.user_id 
            AND usermessage.timestamp = agentmessage.timestamp
        WHERE 
            usermessage.user_id = %s 
        ORDER BY 
            usermessage.timestamp DESC
        LIMIT 3;
    '''

    try :
        conn = psycopg2.connect(SQL_URL)
        cursor = conn.cursor()
        cursor.execute(sql_join ,  user_target)
        data_list = cursor.fetchall()

        cursor.close()
        conn.close()

        print(f"PostgreSQL Selecting Success")
        #print(type(data_list))
        #print(data_list)
        return data_list

    except (Exception, psycopg2.Error) as error:
         print(f"Error PostgreSQL Selecting Fail: {error}")

get_user_messages("U50103dd3166e13e2ffa18b6b2266c77f")