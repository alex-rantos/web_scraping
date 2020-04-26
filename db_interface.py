import psycopg2
import sys
import os

"""
    This table schema is from a past project. Change it to your needs.
    You can use this dictionary technic to have more simple inserts from your main code.
"""

INSERT_DIC = {
    "insertStack": "INSERT INTO stackoverflow(href,title,user_name,likes,views,tags) VALUES(%s,%s,%s,%s,%s,%s)"
}


class PostgresDB(object):

    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", port="5432",
                                     database="web_scraping", user="alex", password="111111")
        self.cur = self.conn.cursor()

    def __create_tables__(self):
        tables = (
            """
            CREATE TABLE stackoverflow (
                id SERIAL PRIMARY KEY,
                href VARCHAR(255) NOT NULL,
                title VARCHAR(255) NOT NULL,
                user_name VARCHAR(255) NOT NULL,
                likes INTEGER NOT NULL,
                views INTEGER NOT NULL,
                tags VARCHAR(255)
            )
            """,)
        for table in tables:
            self.cur.execute(table)

        # commit the changes
        self.conn.commit()

    def __reset__(self):
        self.cur.execute(
            "SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
        rows = self.cur.fetchall()
        for row in rows:
            print("drop table " + row[1])
            self.cur.execute("DROP TABLE " + row[1] + " cascade")
        self.conn.commit()

    def insert_into(self, params, query="insertStack"):
        try:
            response = self.cur.execute(INSERT_DIC[query], params)
            self.conn.commit()
            return response
        except psycopg2.DatabaseError as error:
            print(error)
            return -1

    def __del__(self):
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":
    db = PostgresDB()

    if (len(sys.argv) > 1):
        if (sys.argv[1] == "restart"):
            db.__reset__()
            db.__create_tables__()
            print("Tables recreated")
            exit()
        elif (sys.argv[1] == "reset"):
            db.__reset__()
            print("Tables deleted")
            exit()
        elif (sys.argv[1] == "init"):
            db.__create_tables__()
            print("Tables created")
            exit()
        elif (sys.argv[1] == "insert"):
            href = " @@@"
            title = " dafa"
            user = "dawdaw"
            likes = 2
            views = 2
            tags = "dawdaw"
            params = (href, title, user, likes, views, tags,)
            db.insert_into(params)
            print("Insertion completed")
            exit()
    db.__create_tables__()
    # del db # however it is done automatically when object is out of scope.
