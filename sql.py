import psycopg2
from dotenv import load_dotenv
import os 

load_dotenv()

# host = os.getenv("SQL_HOST")
# port = os.getenv('SQL_PORT')
# user = os.getenv("SQL_USER")
# password = os.getenv("SQL_PASSWORD")

# db_params = {
#     'dbname': 'line_07dg',
#     'user': user,
#     'password': password,
#     'host': host,
#     'port': port,  # PostgreSQL default port is 5432
# }

def postgres_test():
    try:
        conn = psycopg2.connect(**db_params)
        print(conn)
        print(type(conn))
        print("Connected to the PostgreSQL database")
         # 關閉連接
        conn.close()
    except (Exception, psycopg2.Error) as error:
        print(f"Error connecting to PostgreSQL: {error}")

def creat_table():
    try :
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        # 創建表的 SQL 語句
        create_table_query = """
        CREATE TABLE IF NOT EXISTS UserMessage (
            user_id SERIAL PRIMARY KEY,
            message VARCHAR(100),    
        );
        """

        # 執行 SQL 語句
        cursor.execute(create_table_query)
        conn.commit()

        # 關閉連接
        cursor.close()
        conn.close()
    except (Exception, psycopg2.Error) as error:
        print(f"Error PostgreSQL Creating Fail: {error}")

    
postgres_test()