import jwt
import datetime
import os
from dotenv import load_dotenv
import os

load_dotenv()

sql_host = os.getenv('MYSQL_HOST')
sql_user = os.getenv('MYSQL_USER')
sql_password = os.getenv('MYSQL_PASSWORD')
sql_db = os.getenv('MYSQL_DB')

def create_secret_token(user_id):
    token = jwt.encode(
        {'user_id': str(user_id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
        'your_secret_key',
        algorithm='HS256'
    )
    return token

