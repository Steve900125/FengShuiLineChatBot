import psycopg2

DATABASE_URL = "postgres://tester:VZpCHtni9ihQ7x9xpyHAhHbuXUFqiGX9@dpg-codaor8l6cac73bgegeg-a.oregon-postgres.render.com/line_8bak"

conn = psycopg2.connect(DATABASE_URL)
#Replace user and password with your Postgres username and password, host and #port with the values in your database URL, and database_name with the name of #your database.


cur = conn.cursor()

