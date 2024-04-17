from pathlib import Path
import psycopg2
from dotenv import load_dotenv
import os 

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1] 

load_dotenv(ROOT / '.env')

SQL_URL = os.getenv("SQL_URL")

def postgres_test():

    try:
        conn = psycopg2.connect(SQL_URL)
        print(conn)
        print(type(conn))
        print("Connected to the PostgreSQL database")
         # 關閉連接
        conn.close()
    except (Exception, psycopg2.Error) as error:
        print(f"Error connecting to PostgreSQL: {error}")

def creat_table():

    try :
        conn = psycopg2.connect(SQL_URL)
        cursor = conn.cursor()

        # SQL creat user and agent table
        create_user_table_query = """
            CREATE TABLE IF NOT EXISTS UserMessage (
                user_id VARCHAR(40),
                user_message VARCHAR(500),
                timestamp TIMESTAMP   
            );
            """
        create_agent_table_query = """
            CREATE TABLE IF NOT EXISTS AgentMessage (
                user_id VARCHAR(40),
                agent_message VARCHAR(500),
                timestamp TIMESTAMP   
            );
            """
        
        cursor.execute(create_user_table_query)
        cursor.execute(create_agent_table_query)

        conn.commit()

        cursor.close()
        conn.close()
        print(f"PostgreSQL Creating Success")
    except (Exception, psycopg2.Error) as error:
        print(f"Error PostgreSQL Creating Fail: {error}")

def show_db_table():
    conn = psycopg2.connect(SQL_URL)
    cursor = conn.cursor()
    show_query = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public';"

    try:   
        cursor.execute(show_query)
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(table[0])

    except (Exception, psycopg2.Error) as error:
        print(f"Error PostgreSQL Table Show Fail: {error}")
    
    cursor.close()
    conn.close()

def insert_test():

    from datetime import datetime
    curr_dt = datetime.now()
    print("Current datetime: ", curr_dt)
    timestamp = int(round(curr_dt.timestamp()))
    print("Integer timestamp of current datetime: ", timestamp)
    conn = psycopg2.connect(SQL_URL)
    cursor = conn.cursor()
    try:

        insert_sql = '''
            INSERT INTO usermessage(user_id,user_message,timestamp)
            VALUES ('useridtest123451','Goodby world' , %s )
            RETURNING *;
        '''
        timestamp_dt = datetime.fromtimestamp(timestamp)
        timestamp_col = (timestamp_dt,)
        cursor.execute(insert_sql , timestamp_col)
        conn.commit()
       
        print(cursor.fetchall())

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
            agentmessage ON usermessage.user_id = %s 
            AND usermessage.user_id = agentmessage.user_id 
            AND usermessage.timestamp = agentmessage.timestamp;
    '''

    try :
        conn = psycopg2.connect(SQL_URL)
        cursor = conn.cursor()
        cursor.execute(sql_join ,  user_target)
        data_list = cursor.fetchall()
        for user_row in data_list:
            print(user_row[0])
            print(user_row[1])

        cursor.close()
        conn.close()
        print(f"PostgreSQL Selecting Success")
    except (Exception, psycopg2.Error) as error:
         print(f"Error PostgreSQL Selecting Fail: {error}")


if __name__ == "__main__":
    postgres_test()
    creat_table()
    show_db_table()
    insert_test()
    #get_user_messages('U50103dd3166e13e2ffa18b6b2266c77f')
    print(FILE.parents[1])

