import psycopg2
import os
from flask import current_app as app
from psycopg2.extras import RealDictCursor


class DBmigrate:
    def __init__(self):

        self.port = '5432'
        self.host = 'ec2-54-225-242-183.compute-1.amazonaws.com'
        self.db_name = 'dcf13o9ukbb5mm'
        self.user_name = 'koggnwilbyhglb'
        self.user_password = '58039f5f02d2a556522fccc99a424849bb01d98a470bbfd3162661d9a631dc8d'
        
        if os.getenv('DB_NAME') == 'test_epicmail_db':
            self.db_name = 'test_epicmail_db'
            self.user_password = ''
            self.host = '127.0.0.1'
            self.user_name = 'postgres'
        elif os.getenv('DB_NAME') == 'epicmail_db':
            self.db_name = 'epicmail_db'
            self.user_password = 'root'
            self.host = '127.0.0.1'
            self.user_name = 'postgres'
        
        self.db_connect = psycopg2.connect(
            database=self.db_name, user=self.user_name, password=self.user_password, host=self.host, port=self.port)
        self.db_connect.autocommit = True
        self.my_cursor = self.db_connect.cursor(cursor_factory = RealDictCursor)

    def create_tables(self):
        user_table = "CREATE TABLE IF NOT EXISTS users(\
        user_id serial PRIMARY KEY NOT NULL,\
        email_address VARCHAR (30) NOT NULL,\
        first_name VARCHAR (15) DEFAULT 'user',\
        last_name VARCHAR (15),\
        password VARCHAR (15) NOT NULL DEFAULT '12345');"

        email_table = "CREATE TABLE IF NOT EXISTS emails(\
        mail_id serial PRIMARY KEY NOT NULL,\
        created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        subject VARCHAR (20),\
        parent_message_id INT,\
        sender_status VARCHAR (10), \
        reciever_status VARCHAR (10), \
        sender_id INT NOT NULL, \
        reciever_id INT, \
        message_details VARCHAR (60));"

        group_table = "CREATE TABLE IF NOT EXISTS groups(\
        group_id serial PRIMARY KEY,\
        group_name VARCHAR(20) NOT NULL,\
        admin INT NOT NULL,\
        members INT[]);"

        group_email_table = "CREATE TABLE IF NOT EXISTS group_emails(\
        mail_id serial PRIMARY KEY NOT NULL,\
        created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        subject VARCHAR (20),\
        parent_message_id INT,\
        sender_status VARCHAR (10), \
        reciever_status VARCHAR (10), \
        sender_id INT NOT NULL, \
        reciever_id INT, \
        message_details VARCHAR (60));"

        self.db_connect
        self.my_cursor.execute(user_table)
        self.my_cursor.execute(email_table)
        self.my_cursor.execute(group_table)
        self.my_cursor.execute(group_email_table)

    def drop_table(self,table_name):
        dropper = "DROP TABLE IF EXISTS {}".format(table_name)
        self.my_cursor.execute(dropper)

    

