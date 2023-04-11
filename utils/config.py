import os

from dotenv import load_dotenv, find_dotenv

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(find_dotenv(root_path + '/.env'))

# ------------------------------
# |         SQL Server Config  |
# ------------------------------
SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
SQL_PORT = os.getenv('SQL_PORT')

# ------------------------------
# | SPLUNK Config  |
# ------------------------------
SPLUNK_URL = os.getenv('SPLUNK_URL')
SPLUNK_KEY = os.getenv('SPLUNK_KEY')
SPLUNK_HOST = os.getenv('SPLUNK_HOST')
SPLUNK_SOURCE = os.getenv('SPLUNK_SOURCE')

# ------------------------------
# |       Logger Config        |
# ------------------------------
# Logger type   -> persist | show
# Logger Format -> string  | json
LOGGER_TYPE = os.getenv('LOGGER_TYPE')
LOGGER_LEVEL = os.getenv('LOGGER_LEVEL')
LOGGER_FORMAT = os.getenv('LOGGER_FORMAT')

# ------------------------------
# |       MONGO Config        |
# ------------------------------
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_AUTH_MECHANISM = os.getenv('MONGO_AUTH_MECHANISM')
MONGO_REPSET = os.getenv('MONGO_REPSET')
