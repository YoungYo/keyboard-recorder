import json
from db_manager import DbManager
import platform

config = json.load(open('config.json'))
datasource = config['datasource']
db_client = DbManager(datasource['host'], datasource['user'], datasource['port'], datasource['password'], datasource['database'])


PLATFORM = platform.system()
MACOS = 'Darwin'
WINDOWS = 'Windows'
