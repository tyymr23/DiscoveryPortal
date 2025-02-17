import mysql.connector
from flask import request, jsonify
import jwt
from functools import wraps
import os
from dotenv import load_dotenv
import os

load_dotenv()

sql_host = os.getenv('MYSQL_HOST')
sql_user = os.getenv('MYSQL_USER')
sql_password = os.getenv('MYSQL_PASSWORD')
sql_db = os.getenv('MYSQL_DB')



def user_verification(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({'status': False}), 401

        try:
            data = jwt.decode(token, os.getenv("TOKEN_KEY"), algorithms=["HS256"])
            db = mysql.connector.connect(
                host=sql_host,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id=%s", (data['user_id'],))
            user = cursor.fetchone()
            cursor.close()
            db.close()

            if not user:
                return jsonify({'status': False}), 401
            request.user = user
        except jwt.ExpiredSignatureError:
            return jsonify({'status': False, 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'status': False, 'message': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated_function
