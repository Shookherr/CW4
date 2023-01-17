class Config(object):
    DEBUG = True
    JSON_AS_ASCII = False
    # SECRET_HERE = '249y823r9v8238r9u'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 12
    MAX_PAGE = 32
