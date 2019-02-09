import os

SPACES_API_KEY = os.getenv('SPACES_KEY')
SPACES_API_SECRET = os.getenv('SPACES_SECRET')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PW = os.getenv('DB_PASSWORD', 'temppassword')
DB_USER = os.getenv('DB_USER', 'tempuser')
BUCKET_NAME = 'tenpenny-content'
ENDPOINT_URL = 'https://ams3.digitaloceanspaces.com'
