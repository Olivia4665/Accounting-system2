from dotenv import load_dotenv
import os
from app import create_app

load_dotenv()  # Force load .env

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
