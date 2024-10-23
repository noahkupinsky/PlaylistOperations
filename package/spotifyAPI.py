import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")