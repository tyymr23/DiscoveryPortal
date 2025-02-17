from flask import request, jsonify
from functools import wraps
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

sql_host = os.getenv('MYSQL_HOST')
sql_user = os.getenv('MYSQL_USER')
sql_password = os.getenv('MYSQL_PASSWORD')
sql_db = os.getenv('MYSQL_DB')

def check_role(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'user') or not request.user:
                return jsonify({'message': 'User data not available'}), 403

            user_role = request.user.get('role')
            if user_role in roles:
                return f(*args, **kwargs)
            else:
                return jsonify({'message': 'You do not have the required permissions'}), 403
        return decorated_function
    return decorator