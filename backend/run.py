# from app import create_app
# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = create_app()

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=3001, ssl_context=('./certs/localhost.crt', './certs/localhost.key'))


from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)