class DevelopmentConfig():
    DEBUG = True
    SECRET_KEY = 'ArNpixMePI'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'pizza_steve'


config = {
    'development': DevelopmentConfig
}
