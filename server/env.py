MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_USERNAME = "user"
MONGODB_PASSWORD = "password"
MONGODB_DBNAME = "default_db"

from urllib import parse

MONGODB_CONNECTION_URL = f"mongodb://{parse.quote_plus(MONGODB_USERNAME)}:{parse.quote_plus(MONGODB_PASSWORD)}@{parse.quote_plus(MONGODB_HOST)}:{MONGODB_PORT}/{parse.quote_plus(MONGODB_DBNAME)}"
