from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    print("Creating Flask app")

    # Configure MySQL connection
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['MYSQL_PORT'] = os.getenv('MYSQL_PORT')

    # Configure CORS
    CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://tml.cs.vt.edu:3000'], 
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    print("Blueprint registered")

    return app
