import psycopg2

def postgres_test():

    try:
        conn = psycopg2.connect("dbname='line' user='tester' host='127.0.0.1' password='12345' connect_timeout=1 ")
        conn.close()
        print('Done')
        return True
    
    except:
        print('Fail')
        return False

postgres_test()