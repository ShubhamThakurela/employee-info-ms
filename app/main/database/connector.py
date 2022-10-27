import pymysql
from ..database import config

CREDENTIALS = {
    'USERNAME': config.db['user'],
    'PASSWORD': config.db['password'],
    'HOST': config.db['host'],
    'PORT': config.db['port'],
    'DATABASE': config.db['database']
}


# Connection with database
def db_connection():
    try:
        return pymysql.connect(
            host=CREDENTIALS['HOST'],
            user=CREDENTIALS['USERNAME'],
            password=CREDENTIALS['PASSWORD'],
            database=CREDENTIALS['DATABASE'],
            port=CREDENTIALS['PORT']
        )

    except Exception as err:
        # log_error('+++++ Database Connection Issue +++++')
        print((str(err)))

        return False


def db_dict_connection():
    try:
        return pymysql.connect(
            host=CREDENTIALS['HOST'],
            user=CREDENTIALS['USERNAME'],
            passwd=CREDENTIALS['PASSWORD'],
            database=CREDENTIALS['DATABASE'],
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as err:
        # log_error('+++++ Dict Database Connection Issue +++++')
        # log_error(str(err))
        return False
