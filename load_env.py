import os
from dotenv import load_dotenv

load_dotenv()

MY_SQL_USERNAME = os.getenv('MY_SQL_USERNAME')
MY_SQL_PASSWORD = os.getenv('MY_SQL_PASSWORD')
MY_SQL_HOSTNAME = os.getenv('MY_SQL_HOSTNAME')
MY_SQL_PORT = os.getenv('MY_SQL_PORT')
MY_SQL_BD = os.getenv('MY_SQL_BD')

